class LogService {
    constructor() {
      if (LogService.instance) {
        return LogService.instance;
      }
  
      this.logs = [];
      this.webSocket = null;
      this.subscribers = [];
      this.websocketURL = 'ws://127.0.0.1:5000';
      
      this.shouldColorGraph = false;
      
      LogService.instance = this;
    }
  
    openConnection() {
      if (!this.webSocket) {
        this.webSocket = new WebSocket(this.websocketURL);
  
        this.webSocket.onopen = () => {
          console.log('WebSocket connection established');
        };
  
        this.webSocket.onmessage = this.handleSocketMessage.bind(this);
  
        this.webSocket.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
  
        this.webSocket.onclose = () => {
          console.log('WebSocket connection closed');
        };
      }
    }
  
    handleSocketMessage(event) {
      try {
        const rawData = JSON.parse(event.data);
        const logObject = JSON.parse(rawData.log);
  
        this.logs.push(logObject);
        this.subscribers.forEach(callback => callback(this.logs));
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    }
  
    subscribe(callback) {
      this.subscribers.push(callback);
    }
  
    unsubscribe(callback) {
      this.subscribers = this.subscribers.filter(cb => cb !== callback);
    }
  
    getLogs() {
      return this.logs;
    }
  
    closeConnection() {
      if (this.webSocket) {
        this.webSocket.close();
        this.webSocket = null;
      }
    }

    clearLogs() {
      this.logs.splice(0, this.logs.length);
    }

    setShouldColorGraph(value) {
      this.shouldColorGraph = value;
    }

    getShouldColorGraph() {
      return this.shouldColorGraph;
    }
  }
  
  const logService = new LogService();
  export default logService;
  