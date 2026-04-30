# VAME Brainlife App

A Brainlife app that runs the [VAME](https://github.com/EthoML/VAME) pipeline on a list of NWB files containing pose-estimation data. Input is delivered via Brainlife's `neuro/nwb` datatype.

## How it works

1. Reads `config.json`, which Brainlife generates with the `nwb` key set to a list of paths to staged `.nwb` files plus the VAME hyperparameters.
2. Instantiates `VAMEPipeline` with `source_software="NWB"` so VAME loads pose data through `movement-io` from each NWB's `behavior` processing module.
3. Calls `pipeline.run_pipeline(...)` — preprocessing → training set → model training → evaluation → segmentation → community clustering.
4. Generates figures (preprocessing, model losses, UMAP) with `show_figure=False`/`"none"` and `save_to_file=True`.
5. Writes the VAME project tree to `output/<project_name>/` and a summary to `product.json`.

## Local testing

```bash
# edit config.json: set "nwb" to a list of absolute paths to local NWB files,
# drop max_epochs/n_clusters for a smoke test
cp config.json.sample config.json
pip install -r requirements.txt
./main
```

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
