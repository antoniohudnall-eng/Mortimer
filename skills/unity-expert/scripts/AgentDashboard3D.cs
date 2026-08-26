using UnityEngine;
using System.Collections.Generic;
using TMPro;

/// <summary>
/// 3D Dashboard for visualizing agent metrics and system status.
/// Creates a floating, interactive dashboard with real-time data visualization.
/// </summary>
[RequireComponent(typeof(Canvas))]
public class AgentDashboard3D : MonoBehaviour
{
    [Header("Dashboard Settings")]
    [SerializeField] private float updateInterval = 1f;
    [SerializeField] private bool followCamera = true;
    [SerializeField] private float followDistance = 3f;
    [SerializeField] private float heightOffset = 1.5f;
    [SerializeField] private float smoothSpeed = 5f;

    [Header("UI Components")]
    [SerializeField] private TextMeshProUGUI statusText;
    [SerializeField] private TextMeshProUGUI metricsText;
    [SerializeField] private Transform barContainer;
    [SerializeField] private GameObject metricBarPrefab;

    [Header("3D Visualization")]
    [SerializeField] private ParticleSystem activityParticles;
    [SerializeField] private Light statusLight;
    [SerializeField] private Material activeMaterial;
    [SerializeField] private Material idleMaterial;
    [SerializeField] private MeshRenderer dashboardMesh;

    [Header("Data Simulation")]
    [SerializeField] private bool simulateData = true;
    [SerializeField] private float cpuLoad = 0f;
    [SerializeField] private float memoryUsage = 0f;
    [SerializeField] private int activeAgents = 0;

    private Camera mainCamera;
    private List<MetricBar> metricBars = new List<MetricBar>();
    private float updateTimer;
    private Vector3 targetPosition;
    private Quaternion targetRotation;

    // Data structure for metrics
    [System.Serializable]
    public struct SystemMetrics
    {
        public float CPUUsage;
        public float MemoryUsageMB;
        public int ActiveAgentCount;
        public float NetworkLatency;
        public int TasksQueued;
        public string Status;
    }

    [System.Serializable]
    public class MetricBar
    {
        public Transform barTransform;
        public TextMeshProUGUI labelText;
        public TextMeshProUGUI valueText;
        private float currentValue;
        private float targetValue;

        public void UpdateValue(float value)
        {
            targetValue = Mathf.Clamp01(value);
        }

        public void Refresh(float deltaTime)
        {
            currentValue = Mathf.Lerp(currentValue, targetValue, deltaTime * 5f);
            
            if (barTransform != null)
            {
                Vector3 scale = barTransform.localScale;
                scale.x = currentValue;
                barTransform.localScale = scale;
                
                // Color based on value
                var image = barTransform.GetComponent<UnityEngine.UI.Image>();
                if (image != null)
                {
                    image.color = Color.Lerp(Color.green, Color.red, currentValue);
                }
            }
        }
    }

    void Start()
    {
        mainCamera = Camera.main;
        SetupCanvas();
        InitializeMetricBars();
    }

    void SetupCanvas()
    {
        Canvas canvas = GetComponent<Canvas>();
        canvas.renderMode = RenderMode.WorldSpace;
        canvas.worldCamera = mainCamera;
        
        // Scale for world space
        RectTransform rect = canvas.GetComponent<RectTransform>();
        rect.localScale = Vector3.one * 0.005f;
    }

    void InitializeMetricBars()
    {
        string[] metricNames = { "CPU", "Memory", "Agents", "Latency", "Tasks" };
        
        for (int i = 0; i < metricNames.Length; i++)
        {
            GameObject barObj = Instantiate(metricBarPrefab, barContainer);
            MetricBar bar = new MetricBar
            {
                barTransform = barObj.transform.Find("Fill"),
                labelText = barObj.transform.Find("Label").GetComponent<TextMeshProUGUI>(),
                valueText = barObj.transform.Find("Value").GetComponent<TextMeshProUGUI>()
            };
            bar.labelText.text = metricNames[i];
            metricBars.Add(bar);
        }
    }

    void Update()
    {
        // Update data
        updateTimer += Time.deltaTime;
        if (updateTimer >= updateInterval)
        {
            updateTimer = 0f;
            UpdateMetrics();
        }

        // Update visualizations
        UpdateMetricBars();
        Update3DVisualization();
        
        // Follow camera if enabled
        if (followCamera && mainCamera != null)
        {
            FollowCamera();
        }
    }

    void UpdateMetrics()
    {
        if (simulateData)
        {
            // Simulate changing values
            cpuLoad = Mathf.PingPong(Time.time * 0.1f, 1f) + Random.Range(-0.1f, 0.1f);
            memoryUsage = Mathf.PingPong(Time.time * 0.05f + 100f, 500f);
            activeAgents = Mathf.FloorToInt(Mathf.PingPong(Time.time * 0.2f, 20f));
        }
        
        // Update text displays
        if (statusText != null)
        {
            string status = cpuLoad > 0.8f ? "CRITICAL" : cpuLoad > 0.5f ? "BUSY" : "IDLE";
            statusText.text = $"STATUS: <color={(cpuLoad > 0.8f ? "red" : cpuLoad > 0.5f ? "yellow" : "green")}>{status}</color>";
        }

        if (metricsText != null)
        {
            metricsText.text = $"Active Agents: {activeAgents}\nUptime: {Time.time:F0}s";
        }

        // Update bar values
        if (metricBars.Count >= 5)
        {
            metricBars[0].UpdateValue(cpuLoad);
            metricBars[1].UpdateValue(memoryUsage / 1024f); // Normalized
            metricBars[2].UpdateValue(activeAgents / 20f); // Normalized
            metricBars[3].UpdateValue(Random.Range(0.1f, 0.3f)); // Simulated latency
            metricBars[4].UpdateValue(Random.Range(0f, 0.5f)); // Simulated queue
        }
    }

    void UpdateMetricBars()
    {
        foreach (var bar in metricBars)
        {
            bar.Refresh(Time.deltaTime);
        }
    }

    void Update3DVisualization()
    {
        // Update particle emission based on activity
        if (activityParticles != null)
        {
            var emission = activityParticles.emission;
            emission.rateOverTime = cpuLoad * 100f + 10f;
        }

        // Update status light
        if (statusLight != null)
        {
            statusLight.color = Color.Lerp(Color.green, Color.red, cpuLoad);
            statusLight.intensity = Mathf.Lerp(0.5f, 2f, cpuLoad);
        }

        // Update dashboard mesh material
        if (dashboardMesh != null)
        {
            dashboardMesh.material = cpuLoad > 0.5f ? activeMaterial : idleMaterial;
        }
    }

    void FollowCamera()
    {
        // Calculate position in front of camera
        Vector3 cameraForward = mainCamera.transform.forward;
        cameraForward.y = 0; // Keep horizontal
        cameraForward.Normalize();
        
        targetPosition = mainCamera.transform.position + 
                        cameraForward * followDistance + 
                        Vector3.up * heightOffset;
        
        // Billboard rotation
        targetRotation = Quaternion.LookRotation(
            transform.position - mainCamera.transform.position, 
            Vector3.up
        );

        // Smooth movement
        transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime * smoothSpeed);
        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * smoothSpeed);
    }

    // Public API for external data sources
    public void SetMetrics(SystemMetrics metrics)
    {
        simulateData = false;
        cpuLoad = metrics.CPUUsage;
        memoryUsage = metrics.MemoryUsageMB;
        activeAgents = metrics.ActiveAgentCount;
        
        if (statusText != null)
        {
            statusText.text = $"STATUS: {metrics.Status}";
        }
    }

    public void PulseAlert(string message, Color color)
    {
        // Trigger alert animation
        if (statusText != null)
        {
            statusText.text = $"<color=#{ColorUtility.ToHtmlStringRGB(color)}>⚠ {message}</color>";
        }
        
        // Flash light
        if (statusLight != null)
        {
            StartCoroutine(FlashLight(color));
        }
    }

    System.Collections.IEnumerator FlashLight(Color color)
    {
        Color originalColor = statusLight.color;
        float originalIntensity = statusLight.intensity;
        
        statusLight.color = color;
        statusLight.intensity = 5f;
        
        yield return new WaitForSeconds(0.5f);
        
        statusLight.color = originalColor;
        statusLight.intensity = originalIntensity;
    }
}
