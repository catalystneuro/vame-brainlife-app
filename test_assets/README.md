# Test assets

Four jittered NWB files generated from a single DLC source. Each file shares the same keypoint schema (`Nose`, `Forehand-Left/Right`, `Hindhand-Left/Right`, `Tailroot`) but has independent Gaussian noise added to the `(x, y)` positions, so they look like four distinct sessions of the same subject type.

## Uploading to Brainlife

Use the `bl` CLI (faster than the web UI for multiple files).

### One-time setup

```bash
npm install -g brainlife
bl login          # follow the prompt with your brainlife.io credentials
```

### Upload the four NWBs

Get your project ID from the URL when you open the project on brainlife.io:
`https://brainlife.io/project/<PROJECT_ID>/...`

```bash
PROJECT_ID="<paste the hex from the URL>"
for f in *.nwb; do
    subject=$(basename "$f" .nwb)        # session1, session2, ...
    echo "==> Uploading $f as subject=$subject"
    bl data upload \
        --project "$PROJECT_ID" \
        --datatype neuro/nwb \
        --subject "$subject" \
        --nwb "$f"
done
```

Notes:
- `--subject` must be alphanumeric (no spaces). Using the filename stem treats each file as a distinct subject.
- Add `--session <name>` to namespace by session instead.
- Uploaded datasets appear under the project's **Archive** tab; from there the vame-brainlife-app's Submit page lets you tick all four NWBs as the multi-input.

### Web UI alternative

Project page → **Archive** → **Upload** → pick `neuro/nwb` → drop the file → set subject. Repeat per file.
