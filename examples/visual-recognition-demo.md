# Visual Recognition Extension

This demonstrates how the persistent memory system can be extended with visual recognition capabilities for multi-modal AI interactions.

```javascript
// visual-memory.js - Visual recognition extension
class VisualMemoryExtension {
  constructor(memoryManager) {
    this.memory = memoryManager;
    this.faceAPI = null; // Would integrate with face-api.js or similar
    this.initializeFaceRecognition();
  }

  async initializeFaceRecognition() {
    // Initialize face recognition library
    // This would use face-api.js, OpenCV, or similar
    console.log('Initializing face recognition...');
    
    // Load user's face embeddings from memory
    this.loadUserFaceData();
  }

  loadUserFaceData() {
    const faceData = this.memory.memory.visualRecognition?.faceData;
    if (faceData) {
      console.log(`Loaded face recognition data for ${faceData.recognitions} previous recognitions`);
      return faceData;
    }
    
    // Initialize face data structure
    this.memory.memory.visualRecognition = {
      faceData: {
        embeddings: [],
        recognitions: 0,
        lastSeen: null,
        confidence: 0
      },
      visualPreferences: {
        lightingConditions: [],
        cameraAngles: [],
        backgroundTypes: []
      },
      emotionalHistory: [],
      contextualVisuals: []
    };
    
    this.memory.saveMemory();
    return this.memory.memory.visualRecognition.faceData;
  }

  async processVideoFrame(videoElement) {
    try {
      // Detect faces in video frame
      const faces = await this.detectFaces(videoElement);
      
      if (faces.length > 0) {
        const primaryFace = faces[0]; // Use the largest/most centered face
        
        // Generate face embedding
        const embedding = await this.generateFaceEmbedding(primaryFace);
        
        // Check if this matches the user
        const recognition = await this.recognizeUser(embedding);
        
        if (recognition.isUser) {
          this.updateUserRecognition(embedding, recognition.confidence);
          
          // Analyze emotional state
          const emotion = await this.analyzeEmotion(primaryFace);
          this.recordEmotionalState(emotion);
          
          return {
            userRecognized: true,
            confidence: recognition.confidence,
            emotion: emotion,
            timestamp: new Date().toISOString()
          };
        }
      }
      
      return { userRecognized: false };
      
    } catch (error) {
      console.error('Error processing video frame:', error);
      return { error: error.message };
    }
  }

  async detectFaces(videoElement) {
    // Simplified face detection - would use actual face recognition library
    return new Promise((resolve) => {
      // Mock face detection result
      setTimeout(() => {
        resolve([{
          box: { x: 100, y: 100, width: 200, height: 200 },
          landmarks: [], // Facial landmarks
          confidence: 0.95
        }]);
      }, 100);
    });
  }

  async generateFaceEmbedding(face) {
    // Generate numerical representation of face
    // This would use a trained face recognition model
    return new Promise((resolve) => {
      // Mock 512-dimensional face embedding
      const embedding = Array.from({ length: 512 }, () => Math.random());
      resolve(embedding);
    });
  }

  async recognizeUser(newEmbedding) {
    const faceData = this.memory.memory.visualRecognition.faceData;
    
    if (faceData.embeddings.length === 0) {
      // First time seeing user - store their embedding
      faceData.embeddings.push({
        embedding: newEmbedding,
        timestamp: new Date().toISOString(),
        confidence: 1.0
      });
      
      this.memory.saveMemory();
      
      return {
        isUser: true,
        confidence: 1.0,
        firstTime: true
      };
    }
    
    // Calculate similarity with stored embeddings
    let maxSimilarity = 0;
    for (const storedFace of faceData.embeddings) {
      const similarity = this.calculateCosineSimilarity(newEmbedding, storedFace.embedding);
      maxSimilarity = Math.max(maxSimilarity, similarity);
    }
    
    // Threshold for user recognition
    const threshold = 0.7;
    const isUser = maxSimilarity > threshold;
    
    return {
      isUser,
      confidence: maxSimilarity,
      similarity: maxSimilarity
    };
  }

  calculateCosineSimilarity(vec1, vec2) {
    // Calculate cosine similarity between two vectors
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;
    
    for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
      norm1 += vec1[i] * vec1[i];
      norm2 += vec2[i] * vec2[i];
    }
    
    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }

  updateUserRecognition(embedding, confidence) {
    const faceData = this.memory.memory.visualRecognition.faceData;
    
    // Update recognition count
    faceData.recognitions++;
    faceData.lastSeen = new Date().toISOString();
    faceData.confidence = (faceData.confidence + confidence) / 2; // Running average
    
    // Store new embedding if confidence is high
    if (confidence > 0.8) {
      faceData.embeddings.push({
        embedding,
        timestamp: new Date().toISOString(),
        confidence
      });
      
      // Keep only the best 10 embeddings to avoid storage bloat
      faceData.embeddings.sort((a, b) => b.confidence - a.confidence);
      faceData.embeddings = faceData.embeddings.slice(0, 10);
    }
    
    this.memory.saveMemory();
  }

  async analyzeEmotion(face) {
    // Analyze facial expression for emotion
    // This would use an emotion recognition model
    return new Promise((resolve) => {
      const emotions = ['happy', 'sad', 'neutral', 'surprised', 'angry', 'focused'];
      const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
      
      resolve({
        primary: randomEmotion,
        confidence: 0.75 + Math.random() * 0.25,
        allEmotions: {
          happy: Math.random(),
          sad: Math.random(),
          neutral: Math.random(),
          surprised: Math.random(),
          angry: Math.random(),
          focused: Math.random()
        }
      });
    });
  }

  recordEmotionalState(emotion) {
    const emotionalHistory = this.memory.memory.visualRecognition.emotionalHistory;
    
    emotionalHistory.push({
      emotion: emotion.primary,
      confidence: emotion.confidence,
      timestamp: new Date().toISOString(),
      sessionId: this.memory.sessionStartTime
    });
    
    // Keep only last 100 emotional states
    if (emotionalHistory.length > 100) {
      this.memory.memory.visualRecognition.emotionalHistory = emotionalHistory.slice(-100);
    }
    
    this.memory.saveMemory();
  }

  getVisualContext() {
    const visualData = this.memory.memory.visualRecognition;
    
    return {
      userRecognition: {
        totalRecognitions: visualData.faceData.recognitions,
        confidence: visualData.faceData.confidence,
        lastSeen: visualData.faceData.lastSeen
      },
      recentEmotions: visualData.emotionalHistory.slice(-5),
      emotionalTrends: this.analyzeEmotionalTrends(),
      visualPreferences: visualData.visualPreferences
    };
  }

  analyzeEmotionalTrends() {
    const emotions = this.memory.memory.visualRecognition.emotionalHistory;
    if (emotions.length < 5) return null;
    
    const recent = emotions.slice(-10);
    const emotionCounts = {};
    
    recent.forEach(emotion => {
      emotionCounts[emotion.emotion] = (emotionCounts[emotion.emotion] || 0) + 1;
    });
    
    const dominant = Object.entries(emotionCounts)
      .sort(([,a], [,b]) => b - a)[0];
    
    return {
      dominantEmotion: dominant[0],
      frequency: dominant[1] / recent.length,
      trend: this.calculateEmotionalTrend(recent)
    };
  }

  calculateEmotionalTrend(emotions) {
    // Simple trend analysis - could be much more sophisticated
    const positiveEmotions = ['happy', 'surprised'];
    const negativeEmotions = ['sad', 'angry'];
    
    let positiveCount = 0;
    let negativeCount = 0;
    
    emotions.forEach(emotion => {
      if (positiveEmotions.includes(emotion.emotion)) positiveCount++;
      if (negativeEmotions.includes(emotion.emotion)) negativeCount++;
    });
    
    if (positiveCount > negativeCount) return 'positive';
    if (negativeCount > positiveCount) return 'negative';
    return 'neutral';
  }

  // Privacy controls
  clearVisualData() {
    this.memory.memory.visualRecognition = {
      faceData: { embeddings: [], recognitions: 0, lastSeen: null, confidence: 0 },
      visualPreferences: { lightingConditions: [], cameraAngles: [], backgroundTypes: [] },
      emotionalHistory: [],
      contextualVisuals: []
    };
    
    this.memory.saveMemory();
    console.log('All visual recognition data cleared');
  }

  exportVisualData() {
    return {
      visualRecognition: this.memory.memory.visualRecognition,
      exportedAt: new Date().toISOString(),
      privacy: 'user-owned',
      dataTypes: ['faceEmbeddings', 'emotionalHistory', 'visualPreferences']
    };
  }
}

// Enhanced AI Chat with Visual Recognition
class VisualAIChat {
  constructor(userId, videoElement = null) {
    this.memory = new AIMemoryManager(userId);
    this.visualMemory = new VisualMemoryExtension(this.memory);
    this.videoElement = videoElement;
    this.isProcessingVideo = false;
    
    if (videoElement) {
      this.startVisualRecognition();
    }
  }

  async startVisualRecognition() {
    if (this.isProcessingVideo) return;
    
    this.isProcessingVideo = true;
    console.log('Starting visual recognition...');
    
    // Process video frames at regular intervals
    const processFrame = async () => {
      if (this.videoElement && !this.videoElement.paused) {
        const result = await this.visualMemory.processVideoFrame(this.videoElement);
        
        if (result.userRecognized) {
          console.log(`User recognized with ${(result.confidence * 100).toFixed(1)}% confidence`);
          console.log(`Emotional state: ${result.emotion.primary} (${(result.emotion.confidence * 100).toFixed(1)}%)`);
        }
      }
      
      if (this.isProcessingVideo) {
        setTimeout(processFrame, 1000); // Process every second
      }
    };
    
    processFrame();
  }

  stopVisualRecognition() {
    this.isProcessingVideo = false;
    console.log('Visual recognition stopped');
  }

  processMessage(userMessage) {
    // Get both text and visual context
    const textContext = this.memory.getConversationContext();
    const visualContext = this.visualMemory.getVisualContext();
    
    // Generate enhanced response with visual awareness
    const aiResponse = this.generateVisualAwareResponse(userMessage, textContext, visualContext);
    
    // Store interaction with visual context
    this.memory.addInteraction(userMessage, aiResponse, {
      visualContext: visualContext,
      hasVisualRecognition: visualContext.userRecognition.totalRecognitions > 0
    });
    
    return aiResponse;
  }

  generateVisualAwareResponse(userMessage, textContext, visualContext) {
    const responses = [];
    
    // Include visual recognition in response
    if (visualContext.userRecognition.totalRecognitions > 0) {
      responses.push(`I recognize you from our previous video interactions. `);
      
      if (visualContext.recentEmotions.length > 0) {
        const lastEmotion = visualContext.recentEmotions[visualContext.recentEmotions.length - 1];
        responses.push(`I can see you seem ${lastEmotion.emotion} today. `);
      }
    }
    
    // Add context-aware response
    responses.push(`Regarding "${userMessage}", based on our ${textContext.sessionCount} sessions together, I think this relates to your ongoing interests.`);
    
    return responses.join('');
  }

  getFullContext() {
    return {
      textContext: this.memory.getConversationContext(),
      visualContext: this.visualMemory.getVisualContext(),
      memoryStats: this.memory.getMemoryStats()
    };
  }
}

// Example usage
/*
const videoElement = document.getElementById('webcam');
const visualChat = new VisualAIChat('user123', videoElement);

// Start video stream
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    videoElement.srcObject = stream;
    videoElement.play();
  });

// Process a message
const response = visualChat.processMessage('How are you today?');
console.log(response);
*/

module.exports = { VisualMemoryExtension, VisualAIChat };
```

## Integration with Face Recognition Libraries

### Using face-api.js
```javascript
// Real implementation would use face-api.js
import * as faceapi from 'face-api.js';

async function loadFaceAPI() {
  await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
  await faceapi.nets.faceExpressionNet.loadFromUri('/models');
}

async function detectFacesReal(videoElement) {
  const detections = await faceapi
    .detectAllFaces(videoElement, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withFaceDescriptors()
    .withFaceExpressions();
  
  return detections;
}
```

## Privacy and Security Features

### 1. **Local Processing**
- All face recognition happens on user's device
- No face data sent to servers
- User controls all visual data

### 2. **Data Encryption**
```javascript
// Encrypt sensitive visual data
function encryptVisualData(data, userKey) {
  // Use crypto API to encrypt face embeddings
  return crypto.subtle.encrypt('AES-GCM', userKey, JSON.stringify(data));
}
```

### 3. **User Controls**
```javascript
// Privacy controls for visual data
const privacyControls = {
  disableVisualRecognition: () => visualChat.stopVisualRecognition(),
  clearAllVisualData: () => visualChat.visualMemory.clearVisualData(),
  exportVisualData: () => visualChat.visualMemory.exportVisualData(),
  adjustRecognitionSensitivity: (threshold) => setRecognitionThreshold(threshold)
};
```

This visual extension transforms the AI from text-only to truly multi-modal, enabling richer, more natural interactions while maintaining complete user privacy and control.
