using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// Interactive 3D data graph for visualizing time-series data.
/// Supports line graphs, bar charts, and scatter plots.
/// </summary>
[RequireComponent(typeof(LineRenderer))]
public class InteractiveDataGraph : MonoBehaviour
{
    public enum GraphType { Line, Bar, Scatter, Area }
    
    [Header("Graph Configuration")]
    [SerializeField] private GraphType graphType = GraphType.Line;
    [SerializeField] private int maxDataPoints = 50;
    [SerializeField] private Vector3 graphSize = new Vector3(2f, 1.5f, 0.1f);
    [SerializeField] private Color lineColor = Color.cyan;
    [SerializeField] private Color areaColor = new Color(0, 1, 1, 0.3f);
    [SerializeField] private float pointSize = 0.05f;
    
    [Header("Animation")]
    [SerializeField] private bool animateNewPoints = true;
    [SerializeField] private float animationDuration = 0.3f;
    
    [Header("Interaction")]
    [SerializeField] private bool enableInteraction = true;
    [SerializeField] private float hoverScale = 1.2f;
    [SerializeField] private Material lineMaterial;
    [SerializeField] private Material pointMaterial;
    
    [Header("Labels")]
    [SerializeField] private bool showValues = true;
    [SerializeField] private GameObject valueLabelPrefab;
    
    private LineRenderer lineRenderer;
    private List<float> dataValues = new List<float>();
    private List<GameObject> pointObjects = new List<GameObject>();
    private List<GameObject> barObjects = new List<GameObject>();
    private List<GameObject> labelObjects = new List<GameObject>();
    private float maxValue = 100f;
    private Camera mainCamera;

    // Animation tracking
    private class PointAnimation
    {
        public Vector3 targetPosition;
        public Vector3 startPosition;
        public float progress;
        public GameObject pointObject;
    }
    private List<PointAnimation> activeAnimations = new List<PointAnimation>();

    void Start()
    {
        lineRenderer = GetComponent<LineRenderer>();
        mainCamera = Camera.main;
        
        SetupLineRenderer();
        CreateGraphContainer();
    }

    void SetupLineRenderer()
    {
        lineRenderer.useWorldSpace = true;
        lineRenderer.material = lineMaterial != null ? lineMaterial : new Material(Shader.Find("Sprites/Default"));
        lineRenderer.startColor = lineColor;
        lineRenderer.endColor = lineColor;
        lineRenderer.startWidth = 0.02f;
        lineRenderer.endWidth = 0.02f;
        lineRenderer.positionCount = 0;
    }

    void CreateGraphContainer()
    {
        // Create container for organizing child objects
        GameObject container = new GameObject("GraphContainer");
        container.transform.SetParent(transform);
        container.transform.localPosition = Vector3.zero;
    }

    void Update()
    {
        // Update animations
        if (animateNewPoints)
        {
            UpdateAnimations();
        }
        
        // Handle interaction
        if (enableInteraction)
        {
            HandleInteraction();
        }
        
        // Update labels to face camera
        if (showValues)
        {
            UpdateLabelOrientations();
        }
    }

    void UpdateAnimations()
    {
        for (int i = activeAnimations.Count - 1; i >= 0; i--)
        {
            var anim = activeAnimations[i];
            anim.progress += Time.deltaTime / animationDuration;
            
            if (anim.progress >= 1f)
            {
                anim.pointObject.transform.position = anim.targetPosition;
                activeAnimations.RemoveAt(i);
            }
            else
            {
                anim.pointObject.transform.position = Vector3.Lerp(
                    anim.startPosition, 
                    anim.targetPosition, 
                    Mathf.SmoothStep(0, 1, anim.progress)
                );
            }
        }
    }

    void HandleInteraction()
    {
        if (mainCamera == null || !Input.GetMouseButton(0))
            return;

        Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);
        RaycastHit hit;
        
        // Check for hover on points
        foreach (var point in pointObjects)
        {
            if (point == null) continue;
            
            Bounds bounds = new Bounds(point.transform.position, Vector3.one * pointSize * 2f);
            if (bounds.IntersectRay(ray))
            {
                point.transform.localScale = Vector3.one * pointSize * hoverScale;
                
                // Show tooltip
                int index = pointObjects.IndexOf(point);
                if (index >= 0 && index < dataValues.Count)
                {
                    ShowTooltip(point.transform.position, dataValues[index]);
                }
            }
            else
            {
                point.transform.localScale = Vector3.one * pointSize;
            }
        }
    }

    void UpdateLabelOrientations()
    {
        foreach (var label in labelObjects)
        {
            if (label != null && mainCamera != null)
            {
                label.transform.LookAt(label.transform.position + mainCamera.transform.rotation * Vector3.forward,
                                       mainCamera.transform.rotation * Vector3.up);
            }
        }
    }

    /// <summary>
    /// Add a new data point to the graph
    /// </summary>
    public void AddDataPoint(float value)
    {
        dataValues.Add(value);
        
        // Remove old points if exceeding max
        if (dataValues.Count > maxDataPoints)
        {
            dataValues.RemoveAt(0);
            RemoveOldestVisuals();
        }
        
        // Update max value for scaling
        maxValue = Mathf.Max(maxValue, value * 1.2f);
        
        // Rebuild visualization
        RebuildGraph();
    }

    /// <summary>
    /// Add multiple data points at once
    /// </summary>
    public void SetData(float[] values)
    {
        dataValues.Clear();
        ClearVisuals();
        
        foreach (float value in values)
        {
            dataValues.Add(value);
            maxValue = Mathf.Max(maxValue, value * 1.2f);
        }
        
        RebuildGraph();
    }

    void RebuildGraph()
    {
        switch (graphType)
        {
            case GraphType.Line:
                BuildLineGraph();
                break;
            case GraphType.Bar:
                BuildBarChart();
                break;
            case GraphType.Scatter:
                BuildScatterPlot();
                break;
            case GraphType.Area:
                BuildAreaChart();
                break;
        }
    }

    void BuildLineGraph()
    {
        lineRenderer.enabled = true;
        lineRenderer.positionCount = dataValues.Count;
        
        for (int i = 0; i < dataValues.Count; i++)
        {
            Vector3 position = CalculatePointPosition(i, dataValues[i]);
            lineRenderer.SetPosition(i, position);
            
            // Create or update point
            CreateOrUpdatePoint(i, position);
        }
        
        // Remove excess points
        while (pointObjects.Count > dataValues.Count)
        {
            Destroy(pointObjects[pointObjects.Count - 1]);
            pointObjects.RemoveAt(pointObjects.Count - 1);
        }
    }

    void BuildBarChart()
    {
        lineRenderer.enabled = false;
        ClearPoints();
        
        float barWidth = graphSize.x / maxDataPoints * 0.8f;
        
        for (int i = 0; i < dataValues.Count; i++)
        {
            Vector3 basePos = CalculatePointPosition(i, 0);
            float height = (dataValues[i] / maxValue) * graphSize.y;
            
            if (i >= barObjects.Count)
            {
                GameObject bar = GameObject.CreatePrimitive(PrimitiveType.Cube);
                bar.transform.SetParent(transform);
                Destroy(bar.GetComponent<Collider>());
                bar.GetComponent<Renderer>().material = lineMaterial;
                barObjects.Add(bar);
            }
            
            GameObject barObj = barObjects[i];
            barObj.transform.localScale = new Vector3(barWidth, height, graphSize.z);
            barObj.transform.position = basePos + Vector3.up * height / 2f;
        }
        
        // Remove excess bars
        while (barObjects.Count > dataValues.Count)
        {
            Destroy(barObjects[barObjects.Count - 1]);
            barObjects.RemoveAt(barObjects.Count - 1);
        }
    }

    void BuildScatterPlot()
    {
        lineRenderer.enabled = false;
        
        for (int i = 0; i < dataValues.Count; i++)
        {
            float x = (i / (float)(maxDataPoints - 1)) * graphSize.x;
            float y = (dataValues[i] / maxValue) * graphSize.y;
            
            Vector3 position = new Vector3(
                x - graphSize.x / 2f,
                y,
                Random.Range(-graphSize.z / 2f, graphSize.z / 2f)
            );
            
            CreateOrUpdatePoint(i, position);
        }
    }

    void BuildAreaChart()
    {
        // Similar to line but with filled area underneath
        BuildLineGraph();
        
        // Could add mesh generation for filled area here
    }

    Vector3 CalculatePointPosition(int index, float value)
    {
        float x = (index / (float)(maxDataPoints - 1)) * graphSize.x - graphSize.x / 2f;
        float y = (value / maxValue) * graphSize.y;
        float z = 0;
        
        return transform.TransformPoint(new Vector3(x, y, z));
    }

    void CreateOrUpdatePoint(int index, Vector3 position)
    {
        if (index >= pointObjects.Count)
        {
            // Create new point
            GameObject point = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            point.transform.SetParent(transform);
            point.transform.localScale = Vector3.one * pointSize;
            Destroy(point.GetComponent<Collider>());
            
            Renderer rend = point.GetComponent<Renderer>();
            rend.material = pointMaterial != null ? pointMaterial : new Material(Shader.Find("Sprites/Default"));
            rend.material.color = lineColor;
            
            pointObjects.Add(point);
            
            if (animateNewPoints)
            {
                activeAnimations.Add(new PointAnimation
                {
                    pointObject = point,
                    startPosition = position - Vector3.up * graphSize.y,
                    targetPosition = position,
                    progress = 0f
                });
            }
            else
            {
                point.transform.position = position;
            }
            
            // Create label if enabled
            if (showValues)
            {
                CreateValueLabel(index, position, dataValues[index]);
            }
        }
        else
        {
            // Update existing point
            GameObject point = pointObjects[index];
            
            if (animateNewPoints && index == dataValues.Count - 1)
            {
                activeAnimations.Add(new PointAnimation
                {
                    pointObject = point,
                    startPosition = point.transform.position,
                    targetPosition = position,
                    progress = 0f
                });
            }
            else
            {
                point.transform.position = position;
            }
            
            // Update label
            if (showValues && index < labelObjects.Count)
            {
                UpdateValueLabel(index, position, dataValues[index]);
            }
        }
    }

    void CreateValueLabel(int index, Vector3 position, float value)
    {
        if (valueLabelPrefab == null) return;
        
        GameObject label = Instantiate(valueLabelPrefab, transform);
        label.transform.position = position + Vector3.up * 0.1f;
        
        TMPro.TextMeshPro text = label.GetComponent<TMPro.TextMeshPro>();
        if (text != null)
        {
            text.text = value.ToString("F1");
        }
        
        labelObjects.Add(label);
    }

    void UpdateValueLabel(int index, Vector3 position, float value)
    {
        if (index >= labelObjects.Count) return;
        
        GameObject label = labelObjects[index];
        label.transform.position = position + Vector3.up * 0.1f;
        
        TMPro.TextMeshPro text = label.GetComponent<TMPro.TextMeshPro>();
        if (text != null)
        {
            text.text = value.ToString("F1");
        }
    }

    void RemoveOldestVisuals()
    {
        if (pointObjects.Count > 0)
        {
            Destroy(pointObjects[0]);
            pointObjects.RemoveAt(0);
        }
        
        if (labelObjects.Count > 0)
        {
            Destroy(labelObjects[0]);
            labelObjects.RemoveAt(0);
        }
    }

    void ClearPoints()
    {
        foreach (var point in pointObjects)
        {
            if (point != null) Destroy(point);
        }
        pointObjects.Clear();
    }

    void ClearVisuals()
    {
        ClearPoints();
        
        foreach (var bar in barObjects)
        {
            if (bar != null) Destroy(bar);
        }
        barObjects.Clear();
        
        foreach (var label in labelObjects)
        {
            if (label != null) Destroy(label);
        }
        labelObjects.Clear();
        
        lineRenderer.positionCount = 0;
    }

    void ShowTooltip(Vector3 position, float value)
    {
        // Implement tooltip display
        // Could use a world space canvas or draw with Debug
        Debug.DrawLine(position, position + Vector3.up * 0.2f, Color.yellow, 0.1f);
    }

    // Public API
    public void Clear()
    {
        dataValues.Clear();
        ClearVisuals();
    }

    public void SetGraphType(GraphType type)
    {
        graphType = type;
        ClearVisuals();
        RebuildGraph();
    }

    public void SetLineColor(Color color)
    {
        lineColor = color;
        lineRenderer.startColor = color;
        lineRenderer.endColor = color;
    }

    void OnDestroy()
    {
        ClearVisuals();
    }
}
