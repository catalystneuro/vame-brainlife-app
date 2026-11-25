<h1 align="center">VAME Pipeline</h1>

<p align="center">
  Runs the VAME (Variational Animal Motion Embedding) pipeline on NWB files with pose-estimation data to learn behavioral motifs, and outputs the VAME project with segmentations and figures.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.927"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.927-blue.svg" alt="Run on brainlife.io"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Runs the VAME (Variational Animal Motion Embedding) pipeline on NWB files with pose-estimation data to learn behavioral motifs, and outputs the VAME project with segmentations and figures.**

Loads pose data from each NWB file's behavior processing module, preprocesses it (confidence filtering, egocentric alignment, outlier cleaning, Savitzky-Golay smoothing), trains the VAME variational autoencoder, segments behavior into n_clusters motifs with HMM or k-means and runs community clustering. Use it for unsupervised segmentation of animal behavior from pose tracking. It needs NWB files containing ndx-pose PoseEstimation data and a GPU.

| | |
|---|---|
| **Inputs** | `neuro/nwb` |
| **Outputs** | `raw` |
| **Container** | `ghcr.io/catalystneuro/vame-brainlife-app:latest` |
| **Run it** | [doi.org/10.25663/brainlife.app.927](https://doi.org/10.25663/brainlife.app.927) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `nwb` | `neuro/nwb` | yes | NWB files (multi), one per session, containing pose-estimation data. Pose data must be stored as ndx-pose PoseEstimation in the behavior processing module. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `raw` | VAME project directory (output/<project_name>/) with preprocessing results, trained model, segmentations, community clustering and figures. |

<details>
<summary><b>Parameters</b> (14)</summary>

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

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.927](https://doi.org/10.25663/brainlife.app.927), choose `neuro/nwb` from your project, set the parameters and press **Execute**. The results are saved to your project as `raw`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `ghcr.io/catalystneuro/vame-brainlife-app:latest`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "nwb": "/path/to/nwb/nwb",
       "project_name": "vame_project",
       "n_clusters": 15,
       "max_epochs": 10,
       "segmentation_algorithm": "hmm",
       "pose_confidence": 0.9,
       "processing_module_key": "behavior",
       "pose_estimation_key": "PoseEstimation",
       "centered_reference_keypoint": "",
       "orientation_reference_keypoint": "",
       "run_lowconf_cleaning": true,
       "run_egocentric_alignment": true,
       "run_outlier_cleaning": true,
       "run_savgol_filtering": true,
       "run_rescaling": true
   }
   ```

3. Run `./main`.

## How it works

1. Reads `config.json`, which Brainlife generates with the `nwb` key set to a list of paths to staged `.nwb` files plus the VAME hyperparameters.
2. Instantiates `VAMEPipeline` with `source_software="NWB"` so VAME loads pose data through `movement-io` from each NWB's `behavior` processing module.
3. Calls `pipeline.run_pipeline(...)` — preprocessing → training set → model training → evaluation → segmentation → community clustering.
4. Generates figures (preprocessing, model losses, UMAP) with `show_figure=False`/`"none"` and `save_to_file=True`.
5. Writes the VAME project tree to `output/<project_name>/` and a summary to `product.json`.

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- VAME Pipeline. brainlife.io App. [doi:10.25663/brainlife.app.927](https://doi.org/10.25663/brainlife.app.927)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

Maintained by [@catalystneuro](https://github.com/catalystneuro).
