#!/bin/bash
# Complete project formatting script
echo "🎨 Formatting entire Smart News Recommendation System..."

echo "📝 Formatting frontend (React/TypeScript)..."
cd web
npm run format
cd ..

echo "🐍 Formatting backend (Python)..."
cd server
./format.sh
cd ..

echo "📄 Formatting markdown files..."
cd web
npx prettier --write "../*.md"
cd ..

echo "✅ All code has been formatted! Your code is now pretty! 🚀"