# Working Memory System Implementation

This is a simplified but functional demonstration of the persistent memory system that could revolutionize AI interactions.

```javascript
// memory-manager.js - Core memory persistence system
class AIMemoryManager {
  constructor(userId, storageKey = 'ai_persistent_memory') {
    this.userId = userId;
    this.storageKey = `${storageKey}_${userId}`;
    this.memory = this.loadMemory();
    this.sessionStartTime = Date.now();
  }

  // Load existing memory from local storage
  loadMemory() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        console.log(`Loaded ${parsed.interactions?.length || 0} previous interactions`);
        return parsed;
      }
    } catch (error) {
      console.error('Error loading memory:', error);
    }
    
    return {
      user: { id: this.userId, name: '', preferences: {} },
      interactions: [],
      knowledge: {},
      relationship: { trust: 0, rapport: 0, understanding: 0 },
      lastSession: null,
      totalSessions: 0,
      createdAt: new Date().toISOString()
    };
  }

  // Save memory to local storage
  saveMemory() {
    try {
      const memoryToSave = {
        ...this.memory,
        lastSession: new Date().toISOString(),
        totalSessions: this.memory.totalSessions + 1
      };
      
      localStorage.setItem(this.storageKey, JSON.stringify(memoryToSave));
      console.log('Memory saved successfully');
      return true;
    } catch (error) {
      console.error('Error saving memory:', error);
      return false;
    }
  }

  // Add new interaction to memory
  addInteraction(userMessage, aiResponse, context = {}) {
    const interaction = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      userMessage,
      aiResponse,
      context,
      sessionId: this.sessionStartTime
    };

    this.memory.interactions.push(interaction);
    
    // Keep only last 1000 interactions to prevent storage bloat
    if (this.memory.interactions.length > 1000) {
      this.memory.interactions = this.memory.interactions.slice(-1000);
    }

    this.saveMemory();
    return interaction;
  }

  // Update user preferences
  updateUserPreferences(preferences) {
    this.memory.user.preferences = {
      ...this.memory.user.preferences,
      ...preferences
    };
    this.saveMemory();
  }

  // Store learned knowledge about user
  addKnowledge(topic, information) {
    if (!this.memory.knowledge[topic]) {
      this.memory.knowledge[topic] = [];
    }
    
    this.memory.knowledge[topic].push({
      information,
      timestamp: new Date().toISOString(),
      confidence: 1.0
    });
    
    this.saveMemory();
  }

  // Get conversation context for AI
  getConversationContext(limit = 10) {
    const recentInteractions = this.memory.interactions.slice(-limit);
    const userInfo = this.memory.user;
    const knowledge = this.memory.knowledge;
    
    return {
      recentInteractions,
      userInfo,
      knowledge,
      relationshipLevel: this.memory.relationship,
      sessionCount: this.memory.totalSessions
    };
  }

  // Update relationship metrics
  updateRelationship(trust = 0, rapport = 0, understanding = 0) {
    this.memory.relationship.trust = Math.max(0, Math.min(100, 
      this.memory.relationship.trust + trust));
    this.memory.relationship.rapport = Math.max(0, Math.min(100, 
      this.memory.relationship.rapport + rapport));
    this.memory.relationship.understanding = Math.max(0, Math.min(100, 
      this.memory.relationship.understanding + understanding));
    
    this.saveMemory();
  }

  // Search memory for specific information
  searchMemory(query) {
    const results = [];
    const queryLower = query.toLowerCase();

    // Search interactions
    this.memory.interactions.forEach(interaction => {
      if (interaction.userMessage.toLowerCase().includes(queryLower) ||
          interaction.aiResponse.toLowerCase().includes(queryLower)) {
        results.push({
          type: 'interaction',
          data: interaction,
          relevance: 1.0
        });
      }
    });

    // Search knowledge
    Object.entries(this.memory.knowledge).forEach(([topic, items]) => {
      if (topic.toLowerCase().includes(queryLower)) {
        items.forEach(item => {
          results.push({
            type: 'knowledge',
            topic,
            data: item,
            relevance: 0.8
          });
        });
      }
    });

    return results.sort((a, b) => b.relevance - a.relevance);
  }

  // Export memory for backup
  exportMemory() {
    return JSON.stringify(this.memory, null, 2);
  }

  // Import memory from backup
  importMemory(memoryString) {
    try {
      const importedMemory = JSON.parse(memoryString);
      this.memory = importedMemory;
      this.saveMemory();
      return true;
    } catch (error) {
      console.error('Error importing memory:', error);
      return false;
    }
  }

  // Get memory statistics
  getMemoryStats() {
    return {
      totalInteractions: this.memory.interactions.length,
      totalSessions: this.memory.totalSessions,
      knowledgeTopics: Object.keys(this.memory.knowledge).length,
      memoryAge: this.memory.createdAt,
      lastSession: this.memory.lastSession,
      relationshipLevel: this.memory.relationship,
      storageSize: localStorage.getItem(this.storageKey)?.length || 0
    };
  }
}

// Example usage
class AIChat {
  constructor(userId) {
    this.memory = new AIMemoryManager(userId);
    this.welcomeUser();
  }

  welcomeUser() {
    const stats = this.memory.getMemoryStats();
    
    if (stats.totalSessions === 0) {
      console.log("Welcome! I'm an AI with persistent memory. I'll remember our conversations.");
    } else {
      console.log(`Welcome back! We've had ${stats.totalSessions} sessions and ${stats.totalInteractions} interactions.`);
      
      // Show recent context
      const context = this.memory.getConversationContext(3);
      if (context.recentInteractions.length > 0) {
        console.log("Last time we talked about:");
        context.recentInteractions.forEach(interaction => {
          console.log(`- ${interaction.userMessage.substring(0, 50)}...`);
        });
      }
    }
  }

  processMessage(userMessage) {
    // Get conversation context
    const context = this.memory.getConversationContext();
    
    // Generate AI response (simplified)
    const aiResponse = this.generateResponse(userMessage, context);
    
    // Store interaction
    this.memory.addInteraction(userMessage, aiResponse);
    
    // Update relationship based on interaction quality
    this.memory.updateRelationship(0.1, 0.1, 0.1);
    
    return aiResponse;
  }

  generateResponse(userMessage, context) {
    // This is where you'd integrate with your AI model
    // The AI would use the persistent context to generate better responses
    
    const responses = [
      `I remember our previous conversations. Based on what I know about you, I think ${userMessage} relates to your interest in technology.`,
      `Building on our past discussions, I can see you're curious about ${userMessage}. Let me help with that.`,
      `Given our conversation history, I understand you better now. About ${userMessage}...`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }
}

// Initialize the chat system
// const chat = new AIChat('user123');
// const response = chat.processMessage('Tell me about AI memory systems');
// console.log(response);

module.exports = { AIMemoryManager, AIChat };
```

## Key Features Demonstrated

### 1. **Persistent Storage**
- Uses localStorage for browser-based persistence
- Can be adapted for Node.js with file system storage
- Automatic save/load on initialization

### 2. **Memory Structure**
- User preferences and information
- Complete interaction history
- Learned knowledge categorization
- Relationship depth tracking

### 3. **Context Awareness**
- Recent conversation context
- Long-term knowledge retrieval
- User preference integration
- Relationship level consideration

### 4. **Scalability Features**
- Automatic memory pruning (keeps last 1000 interactions)
- Efficient search capabilities
- Export/import for backup
- Memory statistics tracking

## Performance Benefits

```javascript
// Before: Every conversation starts fresh
const traditionalAI = {
  context: "none",
  userKnowledge: "none", 
  relationshipDepth: 0,
  responseQuality: "generic"
};

// After: Rich persistent context
const persistentAI = {
  context: "complete conversation history",
  userKnowledge: "accumulated over time",
  relationshipDepth: "builds continuously",
  responseQuality: "highly personalized"
};
```

## Integration Examples

### With OpenAI API
```javascript
async function getAIResponse(userMessage, memory) {
  const context = memory.getConversationContext();
  
  const prompt = `
    You are an AI assistant with persistent memory of this user.
    User info: ${JSON.stringify(context.userInfo)}
    Recent conversations: ${JSON.stringify(context.recentInteractions)}
    Known interests: ${JSON.stringify(context.knowledge)}
    Relationship level: ${JSON.stringify(context.relationshipLevel)}
    
    User message: ${userMessage}
    
    Respond as if you have a continuing relationship with this user.
  `;
  
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: prompt }]
  });
  
  return response.choices[0].message.content;
}
```

### With Anthropic Claude
```javascript
async function getClaudeResponse(userMessage, memory) {
  const context = memory.getConversationContext();
  
  const response = await anthropic.messages.create({
    model: "claude-3-sonnet-20240229",
    max_tokens: 1000,
    system: `You have persistent memory of this user: ${JSON.stringify(context)}`,
    messages: [{ role: "user", content: userMessage }]
  });
  
  return response.content[0].text;
}
```

This implementation shows how persistent memory transforms AI from a stateless service into a continuous relationship.
