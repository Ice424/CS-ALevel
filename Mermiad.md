```mermaid.js
stateDiagram-v2
        [*] --> Off
        Off --> On :Key turned
        On --> Off :Key turned
        On --> Allarming :Movement Detected
	    Allarming --> Off :Key turned


```

