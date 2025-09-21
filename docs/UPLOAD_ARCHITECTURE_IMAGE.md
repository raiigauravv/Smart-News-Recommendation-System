# Architecture Image Upload Instructions

## To Display the Architecture Diagram on GitHub

1. **Save your architecture image** as `architecture-diagram.png`

2. **Upload to the repository**:
   - Go to your GitHub repository: https://github.com/raiigauravv/Smart-News-Recommendation-System
   - Navigate to `docs/images/` folder
   - Click "Add file" → "Upload files"
   - Upload your `architecture-diagram.png` file
   - Commit the changes

3. **The image will then display** automatically on the README front page

## Alternative: Using Git Commands

```bash
# Copy your architecture image to the docs/images folder
cp /path/to/your/architecture-image.png docs/images/architecture-diagram.png

# Add and commit the image
git add docs/images/architecture-diagram.png
git commit -m "Add system architecture diagram image"
git push origin main
```

## Image Requirements

- **Format**: PNG (recommended) or JPG
- **Filename**: Must be exactly `architecture-diagram.png`
- **Location**: Must be in `docs/images/` folder
- **Size**: Recommended width 800-1200px for best display

Once uploaded, the image will replace the placeholder and display beautifully on your repository's front page!