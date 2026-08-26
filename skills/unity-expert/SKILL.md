---
name: unity-expert
description: Unity 3D development expert — agent visualization, dashboards, and interactive 3D applications.
---

# Unity 3D Development Expert - SKILL.md

**Version:** 1.0  
**Focus:** Unity 6 / 2022.3 LTS for Agent Visualization, Dashboards, and Interactive 3D Applications

---

## Table of Contents

1. [Unity Engine Overview](#unity-engine-overview)
2. [C# Scripting Fundamentals](#c-scripting-fundamentals)
3. [Core Systems](#core-systems)
4. [Physics System](#physics-system)
5. [Animation System](#animation-system)
6. [UI System (UI Toolkit & uGUI)](#ui-system)
7. [Asset Pipeline](#asset-pipeline)
8. [Optimization](#optimization)
9. [Deployment](#deployment)
10. [Agent-Specific Patterns](#agent-specific-patterns)

---

## Unity Engine Overview

### Version Matrix

| Version | Status | Use Case |
|---------|--------|----------|
| Unity 6 | Current (2024+) | New projects, latest features |
| 2022.3 LTS | Stable | Production, long-term support |
| 2021.3 LTS | Legacy | Existing projects |

### Key Unity 6 Features

- **VFX Graph improvements**: Better GPU particle systems
- **ECS (Entity Component System)**: High-performance data-oriented design
- **DOTS Runtime**: Faster runtime with Burst compiler
- **APV (Adaptive Probe Volumes)**: Better lighting for dynamic scenes
- **DLSS/FSR Support**: Upscaling for performance
- **WebGPU backend**: Modern web export
- **SpeedTree 9**: Improved vegetation

### Unity Architecture

```
GameObject (container)
├── Transform (position, rotation, scale)
├── Component A (MonoBehaviour)
├── Component B (MonoBehaviour)
└── Component C (Renderer, Collider, etc.)
```

### Execution Order

```
Awake() → OnEnable() → Start() → FixedUpdate() → Update() → LateUpdate() → OnDisable() → OnDestroy()
```

---

## C# Scripting Fundamentals

### Script Lifecycle

```csharp
public class LifecycleDemo : MonoBehaviour
{
    // Called when script is loaded (even if disabled)
    void Awake()
    {
        Debug.Log("Awake: One-time initialization");
    }
    
    // Called when object becomes active
    void OnEnable()
    {
        Debug.Log("OnEnable: Subscribe to events here");
    }
    
    // Called before first frame (after Awake)
    void Start()
    {
        Debug.Log("Start: Safe to reference other objects");
    }
    
    // Physics updates (fixed timestep, default 50Hz)
    void FixedUpdate()
    {
        // Rigidbody manipulation here
    }
    
    // Once per frame
    void Update()
    {
        // Input, movement, logic
    }
    
    // After all Update calls
    void LateUpdate()
    {
        // Camera follow, final adjustments
    }
    
    // Called when object disabled
    void OnDisable()
    {
        Debug.Log("OnDisable: Unsubscribe from events");
    }
    
    // Called when destroyed
    void OnDestroy()
    {
        Debug.Log("OnDestroy: Cleanup");
    }
}
```

### Component Communication

```csharp
// Method 1: GetComponent (same object)
Rigidbody rb = GetComponent<Rigidbody>();

// Method 2: Find (expensive, cache results)
GameObject player = GameObject.Find("Player");
PlayerController pc = FindObjectOfType<PlayerController>();

// Method 3: Reference in Inspector (preferred)
public class PlayerManager : MonoBehaviour
{
    [SerializeField] private Camera mainCamera;
    [SerializeField] private Transform spawnPoint;
}

// Method 4: Events/Delegates (decoupled)
public static event Action OnPlayerDeath;

// Method 5: Service Locator / Singleton
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    
    void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

### Coroutines for Timing

```csharp
public class CoroutineExamples : MonoBehaviour
{
    // Basic delay
    IEnumerator Start()
    {
        Debug.Log("Waiting...");
        yield return new WaitForSeconds(2f);
        Debug.Log("Done!");
    }
    
    // Repeating with delay
    IEnumerator PulseAnimation()
    {
        while (true)
        {
            yield return StartCoroutine(ScaleUp());
            yield return StartCoroutine(ScaleDown());
        }
    }
    
    // Wait for condition
    IEnumerator WaitForPlayerReady()
    {
        yield return new WaitUntil(() => GameManager.Instance.IsPlayerReady);
        Debug.Log("Player is ready!");
    }
    
    // Wait for coroutine to complete
    IEnumerator Sequence()
    {
        yield return StartCoroutine(PartA());
        yield return StartCoroutine(PartB());
    }
    
    // Stop coroutine
    Coroutine pulseRoutine;
    void StartPulse() => pulseRoutine = StartCoroutine(PulseAnimation());
    void StopPulse() => StopCoroutine(pulseRoutine);
}
```

### Async/Await (Unity 2020+)

```csharp
using System.Threading.Tasks;

public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        await Task.Delay(2000); // Non-blocking delay
        Debug.Log("After delay");
    }
    
    // Unity-specific async helpers
    async Task FadeOutAsync(float duration)
    {
        float elapsed = 0;
        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            float alpha = 1 - (elapsed / duration);
            // Apply alpha...
            await Task.Yield(); // Wait next frame
        }
    }
}
```

---

## Core Systems

### Transform Manipulation

```csharp
public class TransformExamples : MonoBehaviour
{
    void MovementExamples()
    {
        // Move position
        transform.position += Vector3.forward * Time.deltaTime;
        
        // Local space movement
        transform.Translate(Vector3.forward * Time.deltaTime, Space.Self);
        
        // Rotate
        transform.Rotate(0, 90 * Time.deltaTime, 0);
        
        // Look at target
        transform.LookAt(targetTransform);
        
        // Smooth follow
        transform.position = Vector3.Lerp(transform.position, target.position, Time.deltaTime * 5f);
        
        // Smooth damp
        velocity = Vector3.SmoothDamp(transform.position, target.position, ref velocity, 0.3f);
    }
}
```

### Input System (New vs Legacy)

```csharp
// NEW Input System (recommended)
using UnityEngine.InputSystem;

public class NewInputHandler : MonoBehaviour
{
    private InputAction moveAction;
    private InputAction jumpAction;
    
    void OnEnable()
    {
        moveAction = new InputAction("Move", binding: "<Gamepad>/leftStick");
        moveAction.AddBinding("<Keyboard>/w").WithComposite("2DVector").With("Up", "<Keyboard>/w");
        
        moveAction.performed += OnMove;
        moveAction.Enable();
    }
    
    void OnMove(InputAction.CallbackContext context)
    {
        Vector2 input = context.ReadValue<Vector2>();
        // Use input
    }
}

// LEGACY Input (still works)
public class LegacyInput : MonoBehaviour
{
    void Update()
    {
        float horizontal = Input.GetAxis("Horizontal"); // -1 to 1, smooth
        float vertical = Input.GetAxisRaw("Vertical");  // -1, 0, 1, instant
        
        if (Input.GetButtonDown("Jump")) { }
        if (Input.GetKeyDown(KeyCode.Space)) { }
        if (Input.GetMouseButton(0)) { } // Left click
        
        Vector3 mousePos = Input.mousePosition;
        Ray ray = Camera.main.ScreenPointToRay(mousePos);
    }
}
```

### Raycasting

```csharp
public class RaycastExamples : MonoBehaviour
{
    void Update()
    {
        // Basic raycast
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        if (Physics.Raycast(ray, out RaycastHit hit, 100f))
        {
            Debug.Log($"Hit: {hit.collider.name} at {hit.point}");
        }
        
        // Raycast with layer mask
        int layerMask = LayerMask.GetMask("Enemies");
        if (Physics.Raycast(ray, out hit, 100f, layerMask))
        {
            // Only hits objects on "Enemies" layer
        }
        
        // Sphere cast (thickness)
        if (Physics.SphereCast(ray, 0.5f, out hit, 100f))
        {
            // Like raycast but with radius
        }
        
        // Raycast all (multiple hits)
        RaycastHit[] hits = Physics.RaycastAll(ray, 100f);
        
        // Non-allocating version (reuse array)
        RaycastHit[] hitBuffer = new RaycastHit[10];
        int hitCount = Physics.RaycastNonAlloc(ray, hitBuffer, 100f);
    }
}
```

### Object Instantiation & Pooling

```csharp
public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int poolSize = 50;
    
    private Queue<GameObject> pool = new Queue<GameObject>();
    
    void Start()
    {
        // Pre-instantiate
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }
    
    public GameObject Get()
    {
        if (pool.Count > 0)
        {
            GameObject obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        return Instantiate(prefab); // Fallback
    }
    
    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}

// Usage
public class Spawner : MonoBehaviour
{
    [SerializeField] private ObjectPool bulletPool;
    
    void Fire()
    {
        GameObject bullet = bulletPool.Get();
        bullet.transform.position = transform.position;
        bullet.transform.rotation = transform.rotation;
    }
}
```

---

## Physics System

### Rigidbody Types

```csharp
// Dynamic: Full physics simulation
public class DynamicObject : MonoBehaviour
{
    [SerializeField] private Rigidbody rb;
    
    void FixedUpdate()
    {
        // Force-based movement (recommended)
        rb.AddForce(moveDirection * force, ForceMode.Force);
        
        // Instant velocity change
        rb.AddForce(jumpForce, ForceMode.Impulse);
        
        // Direct velocity (use sparingly)
        rb.velocity = newVelocity;
        
        // Rotation
        rb.AddTorque(torque);
        rb.MoveRotation(Quaternion.Euler(rotation));
    }
}

// Kinematic: Controlled by script, affects others
public class MovingPlatform : MonoBehaviour
{
    [SerializeField] private Rigidbody rb;
    
    void Start()
    {
        rb.isKinematic = true; // Enable in Inspector or here
    }
    
    void FixedUpdate()
    {
        // Move via position/rotation
        rb.MovePosition(transform.position + movement);
        rb.MoveRotation(newRotation);
    }
}

// Static: No physics, just collision detection
// (Collider without Rigidbody)
```

### Collision Detection

```csharp
public class CollisionHandler : MonoBehaviour
{
    // Requires non-kinematic Rigidbody
    void OnCollisionEnter(Collision collision)
    {
        Debug.Log($"Collided with {collision.gameObject.name}");
        Debug.Log($"Contact point: {collision.contacts[0].point}");
        Debug.Log($"Impact velocity: {collision.relativeVelocity}");
    }
    
    void OnCollisionStay(Collision collision) { }
    void OnCollisionExit(Collision collision) { }
    
    // Trigger colliders (isTrigger = true)
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Collectible"))
        {
            Collect(other.gameObject);
        }
    }
    
    void OnTriggerStay(Collider other) { }
    void OnTriggerExit(Collider other) { }
}
```

### Physics Queries

```csharp
public class PhysicsQueries : MonoBehaviour
{
    void Examples()
    {
        // Check if position is occupied
        bool occupied = Physics.CheckSphere(position, radius);
        
        // Overlap sphere (all colliders in area)
        Collider[] colliders = Physics.OverlapSphere(center, radius);
        
        // Overlap sphere non-allocating
        Collider[] results = new Collider[10];
        int count = Physics.OverlapSphereNonAlloc(center, radius, results);
        
        // Box cast
        if (Physics.BoxCast(origin, halfExtents, direction, out RaycastHit hit))
        {
            // Hit something with box shape
        }
        
        // Capsule cast
        if (Physics.CapsuleCast(point1, point2, radius, direction, out hit))
        {
            // Hit something with capsule shape
        }
        
        // Line of sight check
        bool hasLineOfSight = !Physics.Linecast(start, end, obstructionMask);
    }
}
```

### Physics Materials

```csharp
// Create via Asset menu: Create > Physics Material
// Properties: Dynamic Friction, Static Friction, Bounciness
// Friction Combine, Bounce Combine (Average, Minimum, Maximum, Multiply)

// Code assignment
Collider col = GetComponent<Collider>();
col.material = Resources.Load<PhysicMaterial>("Materials/Slippery");
```

---

## Animation System

### Animator Controller

```csharp
public class AnimationController : MonoBehaviour
{
    [SerializeField] private Animator animator;
    
    private int isRunningHash;
    private int speedHash;
    
    void Start()
    {
        // Cache parameter hashes (faster than string lookups)
        isRunningHash = Animator.StringToHash("IsRunning");
        speedHash = Animator.StringToHash("Speed");
    }
    
    void Update()
    {
        // Set bool parameter
        animator.SetBool(isRunningHash, isRunning);
        
        // Set float parameter
        animator.SetFloat(speedHash, currentSpeed);
        
        // Set trigger (auto-resets)
        animator.SetTrigger("Jump");
        
        // Reset trigger
        animator.ResetTrigger("Jump");
        
        // Set int
        animator.SetInteger("WeaponType", 2);
        
        // Check state
        bool isInIdle = animator.GetCurrentAnimatorStateInfo(0).IsName("Idle");
        
        // Crossfade (smooth transition)
        animator.CrossFade("Run", 0.25f);
    }
}
```

### Animation Events

```csharp
// Called from animation timeline
public class AnimationEvents : MonoBehaviour
{
    // Called via Animation Event
    public void OnFootstep()
    {
        // Play footstep sound
        AudioManager.Instance.PlayFootstep();
    }
    
    public void OnAttackHit()
    {
        // Check for hits during attack animation
        DetectHit();
    }
}
```

### Blend Trees

```csharp
// In Animator Controller:
// Create Blend Tree → Add Motion fields → Set parameter
// Types: 1D (single parameter), 2D (two parameters)

// Code side
public class BlendTreeController : MonoBehaviour
{
    [SerializeField] private Animator animator;
    
    void Update()
    {
        float x = Input.GetAxis("Horizontal");
        float z = Input.GetAxis("Vertical");
        
        // 2D blend tree parameters
        animator.SetFloat("MoveX", x);
        animator.SetFloat("MoveZ", z);
        
        // Or combined
        Vector3 move = new Vector3(x, 0, z);
        animator.SetFloat("Speed", move.magnitude);
    }
}
```

### Timeline (Cinemachine + Timeline)

```csharp
using UnityEngine.Playables;
using UnityEngine.Timeline;

public class CutsceneController : MonoBehaviour
{
    [SerializeField] private PlayableDirector director;
    
    void PlayCutscene()
    {
        director.Play();
    }
    
    void BindCamera(Cinemachine.CinemachineVirtualCamera vcam)
    {
        // Bind timeline track to runtime object
        var timeline = director.playableAsset as TimelineAsset;
        // ... binding code
    }
}
```

---

## UI System

### UI Toolkit (Modern, recommended)

```csharp
using UnityEngine.UIElements;

public class UIToolkitController : MonoBehaviour
{
    [SerializeField] private UIDocument uiDocument;
    
    private VisualElement root;
    private Label statusLabel;
    private Button actionButton;
    private ProgressBar healthBar;
    
    void OnEnable()
    {
        root = uiDocument.rootVisualElement;
        
        // Query elements by name or class
        statusLabel = root.Q<Label>("status-label");
        actionButton = root.Q<Button>("action-btn");
        healthBar = root.Q<ProgressBar>("health-bar");
        
        // Register callbacks
        actionButton.clicked += OnActionClicked;
        
        // USS styling
        statusLabel.AddToClassList("highlight");
    }
    
    void OnDisable()
    {
        actionButton.clicked -= OnActionClicked;
    }
    
    void OnActionClicked()
    {
        // Handle click
    }
    
    // Dynamic content
    void UpdateHealth(float current, float max)
    {
        healthBar.value = current;
        healthBar.highValue = max;
        healthBar.title = $"{current}/{max}";
    }
    
    // Create elements dynamically
    VisualElement CreateStatRow(string name, float value)
    {
        var row = new VisualElement();
        row.AddToClassList("stat-row");
        
        var nameLabel = new Label(name);
        var valueLabel = new Label(value.ToString("F1"));
        
        row.Add(nameLabel);
        row.Add(valueLabel);
        
        return row;
    }
}
```

### uGUI (Legacy, still common)

```csharp
using UnityEngine.UI;
using TMPro;

public class UGUIController : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI titleText;
    [SerializeField] private Slider progressSlider;
    [SerializeField] private Button submitButton;
    [SerializeField] private Image healthBar;
    
    void Start()
    {
        // Button click
        submitButton.onClick.AddListener(OnSubmit);
        
        // Slider change
        progressSlider.onValueChanged.AddListener(OnProgressChanged);
        
        // Text formatting
        titleText.text = $"Score: <color=green>{score}</color>";
        
        // Image fill
        healthBar.fillAmount = currentHealth / maxHealth;
    }
    
    void OnSubmit()
    {
        Debug.Log("Submitted!");
    }
    
    void OnProgressChanged(float value)
    {
        Debug.Log($"Progress: {value:P0}");
    }
}
```

### World Space UI (for 3D dashboards)

```csharp
public class WorldSpaceUI : MonoBehaviour
{
    [SerializeField] private Canvas canvas;
    [SerializeField] private Transform target;
    [SerializeField] private Vector3 offset;
    
    void Start()
    {
        // Configure for world space
        canvas.renderMode = RenderMode.WorldSpace;
        canvas.worldCamera = Camera.main;
        
        // Scale down (world space units)
        RectTransform rect = canvas.GetComponent<RectTransform>();
        rect.sizeDelta = new Vector2(400, 200);
        rect.localScale = Vector3.one * 0.01f;
    }
    
    void LateUpdate()
    {
        // Follow target
        transform.position = target.position + offset;
        
        // Billboard - face camera
        transform.LookAt(transform.position + Camera.main.transform.rotation * Vector3.forward,
                         Camera.main.transform.rotation * Vector3.up);
    }
}
```

---

## Asset Pipeline

### Importing Assets

```yaml
# Supported formats:
Models:
  - FBX (recommended)
  - OBJ
  - glTF/glb
  - DAE (Collada)
  
Textures:
  - PNG, JPEG, TGA, TIFF, PSD
  - HDR/EXR for skyboxes
  
Audio:
  - WAV, MP3, OGG, AIFF
  
Video:
  - MP4, WEBM, MOV
```

### Import Settings via Script

```csharp
using UnityEditor;

public class AssetImporterTools
{
    // Configure texture import
    [MenuItem("Tools/Configure Texture")]
    static void ConfigureTexture()
    {
        string path = "Assets/Textures/mytexture.png";
        TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
        
        importer.textureType = TextureImporterType.Sprite;
        importer.spritePixelsPerUnit = 100;
        importer.filterMode = FilterMode.Point; // Pixel art
        importer.textureCompression = TextureImporterCompression.Compressed;
        
        importer.SaveAndReimport();
    }
    
    // Configure model import
    [MenuItem("Tools/Configure Model")]
    static void ConfigureModel()
    {
        string path = "Assets/Models/mymodel.fbx";
        ModelImporter importer = AssetImporter.GetAtPath(path) as ModelImporter;
        
        importer.animationType = ModelImporterAnimationType.Human;
        importer.materialImportMode = ModelImporterMaterialImportMode.ImportStandard;
        
        // LOD settings
        importer.generateSecondaryUV = true;
        importer.secondaryUVAngleDistortion = 8;
        importer.secondaryUVAreaDistortion = 15;
        
        importer.SaveAndReimport();
    }
}
#endif
```

### Addressable Assets (Runtime loading)

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AddressableLoader : MonoBehaviour
{
    // Reference in Inspector
    [SerializeField] private AssetReferenceGameObject enemyPrefab;
    
    // Or load by key
    AsyncOperationHandle<GameObject> handle;
    
    async void LoadAsset()
    {
        // Single asset
        handle = Addressables.LoadAssetAsync<GameObject>("Enemy_Boss");
        GameObject prefab = await handle.Task;
        
        Instantiate(prefab);
        
        // Release when done
        Addressables.Release(handle);
    }
    
    // Load with dependencies
    async void LoadScene()
    {
        var op = Addressables.LoadSceneAsync("Level_02", UnityEngine.SceneManagement.LoadSceneMode.Additive);
        await op.Task;
    }
}
```

---

## Optimization

### Profiler & Debugging

```csharp
public class PerformanceTools : MonoBehaviour
{
    void Update()
    {
        // Custom profiler markers
        Profiler.BeginSample("MyCustomUpdate");
        
        // Expensive operation here
        
        Profiler.EndSample();
    }
    
    void MemoryInfo()
    {
        long totalMemory = GC.GetTotalMemory(false);
        Debug.Log($"Managed memory: {totalMemory / 1024 / 1024} MB");
        
        long usedMemory = Profiler.GetTotalAllocatedMemory(false);
        Debug.Log($"Total allocated: {usedMemory / 1024 / 1024} MB");
    }
}
```

### Common Optimizations

```csharp
public class OptimizedScript : MonoBehaviour
{
    // Cache component lookups
    private Transform cachedTransform;
    private Rigidbody cachedRigidbody;
    
    void Awake()
    {
        cachedTransform = transform;
        cachedRigidbody = GetComponent<Rigidbody>();
    }
    
    void Update()
    {
        // Use cached reference
        cachedTransform.position += Vector3.forward * Time.deltaTime;
    }
    
    // Avoid GetComponent in Update
    // BAD: GetComponent<Rigidbody>().AddForce(force);
    // GOOD: cachedRigidbody.AddForce(force);
    
    // Cache hash lookups
    private static readonly int SpeedHash = Animator.StringToHash("Speed");
    
    // Use object pooling (see above)
    
    // Use Job System for heavy computations
    
    // GPU Instancing for repeated meshes
    // Material.EnableKeyword("_INSTANCING_ON");
}
```

### Culling & LOD

```csharp
// LOD Group setup
public class LODSetup : MonoBehaviour
{
    void SetupLOD()
    {
        LODGroup lodGroup = gameObject.AddComponent<LODGroup>();
        
        LOD[] lods = new LOD[3];
        
        // LOD 0: 100% - 60% screen coverage
        Renderer[] renderers0 = GetLOD0Renderers();
        lods[0] = new LOD(0.6f, renderers0);
        
        // LOD 1: 60% - 30%
        Renderer[] renderers1 = GetLOD1Renderers();
        lods[1] = new LOD(0.3f, renderers1);
        
        // LOD 2: 30% - 10%
        Renderer[] renderers2 = GetLOD2Renderers();
        lods[2] = new LOD(0.1f, renderers2);
        
        lodGroup.SetLODs(lods);
        lodGroup.RecalculateBounds();
    }
}
```

### Burst & Job System

```csharp
using Unity.Collections;
using Unity.Jobs;
using Unity.Mathematics;
using Unity.Burst;

// Burst-compiled job
[BurstCompile]
public struct MoveJob : IJobParallelFor
{
    [ReadOnly] public float deltaTime;
    public NativeArray<float3> positions;
    [ReadOnly] public NativeArray<float3> velocities;
    
    public void Execute(int index)
    {
        positions[index] += velocities[index] * deltaTime;
    }
}

public class JobSystemExample : MonoBehaviour
{
    NativeArray<float3> positions;
    NativeArray<float3> velocities;
    
    void Update()
    {
        // Schedule job
        MoveJob job = new MoveJob
        {
            deltaTime = Time.deltaTime,
            positions = positions,
            velocities = velocities
        };
        
        JobHandle handle = job.Schedule(positions.Length, 64);
        handle.Complete();
    }
    
    void OnDestroy()
    {
        positions.Dispose();
        velocities.Dispose();
    }
}
```

---

## Deployment

### Build Pipeline

```csharp
using UnityEditor;
using UnityEditor.Build.Reporting;

public class BuildTools
{
    [MenuItem("Build/Build Windows")]
    static void BuildWindows()
    {
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            locationPathName = "Builds/Windows/MyGame.exe",
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        };
        
        BuildReport report = BuildPipeline.BuildPlayer(options);
        BuildSummary summary = report.summary;
        
        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log($"Build succeeded: {summary.totalSize / 1024 / 1024} MB");
        }
    }
    
    [MenuItem("Build/Build WebGL")]
    static void BuildWebGL()
    {
        // WebGL-specific settings
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Gzip;
        PlayerSettings.WebGL.exceptionSupport = WebGLExceptionSupport.FullWithStacktrace;
        
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            locationPathName = "Builds/WebGL",
            target = BuildTarget.WebGL,
            options = BuildOptions.None
        };
        
        BuildPipeline.BuildPlayer(options);
    }
    
    static string[] GetScenePaths()
    {
        return EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();
    }
}
#endif
```

### Cloud Build & CI/CD

```yaml
# .github/workflows/unity-build.yml
name: Unity Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: game-ci/unity-builder@v3
        with:
          targetPlatform: WebGL
          unityVersion: 2022.3.x
          
      - uses: actions/upload-artifact@v3
        with:
          name: Build
          path: build
```

---

## Agent-Specific Patterns

### Data Visualization Dashboard

```csharp
// Real-time data visualization for agent metrics
public class AgentDashboard : MonoBehaviour
{
    [Header("UI References")]
    [SerializeField] private LineGraph cpuGraph;
    [SerializeField] private BarChart memoryChart;
    [SerializeField] private TextMeshProUGUI statusText;
    
    [Header("3D Visualization")]
    [SerializeField] private Transform nodeContainer;
    [SerializeField] private GameObject nodePrefab;
    
    private Dictionary<string, NodeVisualizer> activeNodes = new();
    
    void Update()
    {
        // Poll agent metrics
        var metrics = AgentAPI.GetMetrics();
        
        // Update graphs
        cpuGraph.AddDataPoint(metrics.CPUUsage);
        memoryChart.SetValue(metrics.MemoryUsage);
        
        // Update 3D nodes
        foreach (var node in metrics.Nodes)
        {
            if (!activeNodes.ContainsKey(node.Id))
            {
                CreateNode(node);
            }
            activeNodes[node.Id].UpdateState(node);
        }
    }
    
    void CreateNode(NodeData data)
    {
        GameObject nodeObj = Instantiate(nodePrefab, nodeContainer);
        var visualizer = nodeObj.GetComponent<NodeVisualizer>();
        visualizer.Initialize(data);
        activeNodes[data.Id] = visualizer;
    }
}
```

### Interactive 3D Widget

```csharp
// Draggable, interactive 3D widget
[RequireComponent(typeof(Rigidbody))]
public class InteractiveWidget : MonoBehaviour, IPointerClickHandler, IDragHandler
{
    [SerializeField] private Color normalColor = Color.white;
    [SerializeField] private Color hoverColor = Color.cyan;
    [SerializeField] private Color selectedColor = Color.green;
    
    private Renderer rend;
    private MaterialPropertyBlock propBlock;
    private bool isSelected;
    
    void Awake()
    {
        rend = GetComponent<Renderer>();
        propBlock = new MaterialPropertyBlock();
    }
    
    public void OnPointerClick(PointerEventData eventData)
    {
        isSelected = !isSelected;
        SetColor(isSelected ? selectedColor : normalColor);
        
        if (isSelected)
        {
            OnWidgetSelected?.Invoke(this);
        }
    }
    
    public void OnDrag(PointerEventData eventData)
    {
        // Raycast from mouse to find world position
        Ray ray = Camera.main.ScreenPointToRay(eventData.position);
        if (Physics.Raycast(ray, out RaycastHit hit, 100f, dragPlaneLayer))
        {
            transform.position = hit.point + Vector3.up * 0.5f;
        }
    }
    
    void SetColor(Color color)
    {
        rend.GetPropertyBlock(propBlock);
        propBlock.SetColor("_Color", color);
        rend.SetPropertyBlock(propBlock);
    }
    
    public static event Action<InteractiveWidget> OnWidgetSelected;
}
```

### Network Graph Visualization

```csharp
// 3D network graph for agent relationships
public class NetworkGraph : MonoBehaviour
{
    [SerializeField] private NodeVisual nodePrefab;
    [SerializeField] private LineRenderer edgePrefab;
    
    private List<NodeVisual> nodes = new();
    private List<LineRenderer> edges = new();
    
    public void BuildGraph(GraphData data)
    {
        ClearGraph();
        
        // Create nodes
        foreach (var nodeData in data.Nodes)
        {
            var node = Instantiate(nodePrefab, transform);
            node.transform.localPosition = nodeData.Position;
            node.SetLabel(nodeData.Name);
            node.SetColor(GetColorForType(nodeData.Type));
            nodes.Add(node);
        }
        
        // Create edges
        foreach (var edgeData in data.Edges)
        {
            var edge = Instantiate(edgePrefab, transform);
            edge.positionCount = 2;
            edge.SetPosition(0, nodes[edgeData.Source].transform.position);
            edge.SetPosition(1, nodes[edgeData.Target].transform.position);
            edge.startColor = edge.endColor = Color.gray;
            edges.Add(edge);
        }
    }
    
    void Update()
    {
        // Animate edges (pulse effect)
        float pulse = Mathf.PingPong(Time.time * 2, 1);
        foreach (var edge in edges)
        {
            edge.startWidth = edge.endWidth = 0.02f + pulse * 0.01f;
        }
    }
}
```

---

## Quick Reference

### Common Attributes

| Attribute | Purpose |
|-----------|---------|
| `[SerializeField]` | Show in Inspector without public |
| `[HideInInspector]` | Hide public field from Inspector |
| `[Range(min, max)]` | Slider in Inspector |
| `[Header("Text")]` | Section header in Inspector |
| `[Tooltip("Text")]` | Hover tooltip |
| `[RequireComponent(Type)]` | Auto-add components |
| `[ExecuteInEditMode]` | Run in Editor |

### Useful Shortcuts

```csharp
// Quick references
Camera.main                    // Main camera
Time.deltaTime                // Frame duration
Time.time                     // Seconds since start
Time.timeScale                // Simulation speed (0 = pause)
Screen.width/height           // Display resolution
Input.mousePosition           // Mouse in pixels
Random.Range(min, max)        // Random number
Mathf.Lerp(a, b, t)           // Linear interpolation
Mathf.SmoothDamp()            // Smooth value transition
Quaternion.Slerp()            // Smooth rotation
Vector3.Distance(a, b)        // Distance between points
```

### Layer Mask Operations

```csharp
// Create layer mask
int enemyMask = LayerMask.GetMask("Enemies");
int obstacleMask = 1 << LayerMask.NameToLayer("Obstacle");
int combined = enemyMask | obstacleMask;

// Check layer
bool isEnemy = gameObject.layer == LayerMask.NameToLayer("Enemies");
```

---

## Resources

- **Documentation:** https://docs.unity3d.com/
- **Scripting API:** https://docs.unity3d.com/ScriptReference/
- **Unity Learn:** https://learn.unity.com/
- **Asset Store:** https://assetstore.unity.com/
- **C# Reference:** https://docs.microsoft.com/en-us/dotnet/csharp/
