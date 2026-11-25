# VAME Brainlife App

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Runs the VAME (Variational Animal Motion Embedding) pipeline on NWB files with pose-estimation data to learn behavioral motifs, and outputs the VAME project with segmentations and figures.**

Loads pose data from each NWB file's behavior processing module, preprocesses it (confidence filtering, egocentric alignment, outlier cleaning, Savitzky-Golay smoothing), trains the VAME variational autoencoder, segments behavior into n_clusters motifs with HMM or k-means and runs community clustering. Use it for unsupervised segmentation of animal behavior from pose tracking. It needs NWB files containing ndx-pose PoseEstimation data and a GPU.

| | |
|---|---|
| 📥 **Inputs** | `neuro/nwb` |
| 📤 **Outputs** | `raw` |
| 🐳 **Container** | `ghcr.io/catalystneuro/vame-brainlife-app:latest` |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.927](https://doi.org/10.25663/brainlife.app.927) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `nwb` | `neuro/nwb` | yes | NWB files (multi), one per session, containing pose-estimation data. Pose data must be stored as ndx-pose PoseEstimation in the behavior processing module. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `raw` | VAME project directory (output/<project_name>/) with preprocessing results, trained model, segmentations, community clustering and figures. |

<details>
<summary><b>⚙️ Parameters</b> (14)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `project_name` | string | `vame_project` | VAME project directory name |
| `n_clusters` | number | `15` | Number of motifs |
| `max_epochs` | number | `10` | Number of maximum training epochs |
| `segmentation_algorithm` | enum | `hmm` | Segmentation algorithm Options: `hmm`, `kmeans`. |
| `pose_confidence` | number | `0.9` | Confidence threshold for pose filtering |
| `processing_module_key` | string | `behavior` | NWB processing module containing pose data |
| `pose_estimation_key` | string | `PoseEstimation` | ndx_pose.PoseEstimation container name |
| `centered_reference_keypoint` | string |  | Keypoint name for egocentric centering |
| `orientation_reference_keypoint` | string |  | Keypoint name for egocentric orientation |
| `run_lowconf_cleaning` | boolean | `true` | Drop low-confidence frames during preprocessing |
| `run_egocentric_alignment` | boolean | `true` | Align poses egocentrically (uses centered + orientation keypoints) |
| `run_outlier_cleaning` | boolean | `true` | Clean outlier keypoints |
| `run_savgol_filtering` | boolean | `true` | Apply Savitzky-Golay smoothing |
| `run_rescaling` | boolean | `true` | rescale poses |

</details>

<!-- brainlife-app:end -->

A Brainlife app that runs the [VAME](https://github.com/EthoML/VAME) pipeline on a list of NWB files containing pose-estimation data. Input is delivered via Brainlife's `neuro/nwb` datatype.

## How it works

1. Reads `config.json`, which Brainlife generates with the `nwb` key set to a list of paths to staged `.nwb` files plus the VAME hyperparameters.
2. Instantiates `VAMEPipeline` with `source_software="NWB"` so VAME loads pose data through `movement-io` from each NWB's `behavior` processing module.
3. Calls `pipeline.run_pipeline(...)` — preprocessing → training set → model training → evaluation → segmentation → community clustering.
4. Generates figures (preprocessing, model losses, UMAP) with `show_figure=False`/`"none"` and `save_to_file=True`.
5. Writes the VAME project tree to `output/<project_name>/` and a summary to `product.json`.


## Brainlife registration

- **Input datatype**: [`neuro/nwb`](https://brainlife.io/datatype/69f24b375e3b9b921dc25e49) — file `data.nwb` mapped to key `nwb`.
- **Config params**:
  - `project_name` (string) — VAME project directory name
  - `n_clusters` (int) — number of motifs/states
  - `max_epochs` (int) — VAE training epochs
  - `segmentation_algorithm` (enum: `"hmm"` | `"kmeans"`) — segmentation algorithm
  - `pose_confidence` (float) — confidence threshold for pose filtering
  - `processing_module_key` (string, default `"behavior"`) — NWB processing module containing pose data
  - `pose_estimation_key` (string, default `"PoseEstimation"`) — `ndx_pose.PoseEstimation` container name
  - `centered_reference_keypoint` (string or null) — keypoint name for egocentric centering (VAME default: `"snout"`)
  - `orientation_reference_keypoint` (string or null) — keypoint name for egocentric orientation (VAME default: `"tailbase"`)
  - `run_lowconf_cleaning` (bool) — drop low-confidence frames during preprocessing
  - `run_egocentric_alignment` (bool) — align poses egocentrically (uses centered + orientation keypoints)
  - `run_outlier_cleaning` (bool) — clean outlier keypoints
  - `run_savgol_filtering` (bool) — apply Savitzky-Golay smoothing
  - `run_rescaling` (bool) — rescale poses (default `false`)
- **Output**: `raw` datatype, output directory `output/<project_name>/`.
- **Resources**: GPU required.
