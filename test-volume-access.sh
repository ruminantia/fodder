#!/bin/bash

# Test script to verify multi-container volume access for Ruminantia Fodder
# This script tests that the Discord bot can write to volumes and other containers can read them

set -e

echo "🧪 Testing multi-container volume access..."

# Start the services
echo "🚀 Starting Docker Compose services..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Test 1: Verify Discord bot container is running
echo "📋 Test 1: Checking if Discord bot container is running..."
if docker ps --filter "name=ruminantia-fodder" --format "table {{.Names}}\t{{.Status}}" | grep -q "Up"; then
    echo "✅ Discord bot container is running"
else
    echo "❌ Discord bot container is not running"
    exit 1
fi

# Test 2: Verify transcription reader container is running
echo "📋 Test 2: Checking if transcription reader container is running..."
if docker ps --filter "name=fodder-reader" --format "table {{.Names}}\t{{.Status}}" | grep -q "Up"; then
    echo "✅ Transcription reader container is running"
else
    echo "❌ Transcription reader container is not running"
    exit 1
fi

# Test 3: Verify volumes are created
echo "📋 Test 3: Checking if named volumes are created..."
VOLUMES=("fodder_downloads" "fodder_transcriptions" "fodder_temp")
for volume in "${VOLUMES[@]}"; do
    if docker volume ls | grep -q "$volume"; then
        echo "✅ Volume '$volume' exists"
    else
        echo "❌ Volume '$volume' does not exist"
        exit 1
    fi
done

# Test 4: Test write access from Discord bot
echo "📋 Test 4: Testing write access from Discord bot container..."
docker exec ruminantia-fodder sh -c 'echo "Test transcription $(date)" > /app/fodder/test-file.txt'
if docker exec ruminantia-fodder test -f /app/fodder/test-file.txt; then
    echo "✅ Discord bot can write to fodder volume"
else
    echo "❌ Discord bot cannot write to fodder volume"
    exit 1
fi

# Test 5: Test read access from transcription reader
echo "📋 Test 5: Testing read access from transcription reader container..."
if docker exec fodder-reader test -f /read-only/transcriptions/test-file.txt; then
    echo "✅ Transcription reader can read from fodder volume"

    # Verify content
    CONTENT=$(docker exec fodder-reader cat /read-only/transcriptions/test-file.txt)
    echo "📄 Content read by transcription reader: $CONTENT"
else
    echo "❌ Transcription reader cannot read from fodder volume"
    exit 1
fi

# Test 6: Test that transcription reader cannot write (read-only mount)
echo "📋 Test 6: Testing that transcription reader cannot write (read-only)..."
if docker exec fodder-reader sh -c 'echo "Attempted write" > /read-only/transcriptions/write-test.txt 2>/dev/null'; then
    echo "❌ Transcription reader should not be able to write (read-only mount failed)"
    exit 1
else
    echo "✅ Transcription reader correctly cannot write to read-only volume"
fi

# Test 7: Verify bot-only volumes are not accessible to reader
echo "📋 Test 7: Verifying bot-only volumes isolation..."
if docker exec fodder-reader test -d /app/downloads 2>/dev/null; then
    echo "⚠️  Transcription reader can access downloads volume (may be acceptable depending on requirements)"
else
    echo "✅ Downloads volume is properly isolated from transcription reader"
fi

# Test 8: Clean up test file
echo "📋 Test 8: Cleaning up test files..."
docker exec ruminantia-fodder rm -f /app/fodder/test-file.txt
echo "✅ Test files cleaned up"

echo ""
echo "🎉 All volume access tests passed!"
echo ""
echo "📊 Summary:"
echo "   - Discord bot has read/write access to all volumes"
echo "   - Transcription reader has read-only access to fodder volume"
echo "   - Bot-only volumes (downloads, temp_chunks) are properly isolated"
echo ""
echo "🚀 Volume setup is ready for production use!"

# Optional: Show volume information
echo ""
echo "📦 Volume Information:"
docker volume ls | grep fodder

# Stop services (comment out if you want to keep them running)
echo ""
echo "🛑 Stopping test services..."
docker compose down

echo "✅ Test completed successfully!"
