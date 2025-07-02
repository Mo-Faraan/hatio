import Button from "./Button";

export default function Generated({generatedJSON,copyStatus,onCopy}) {
    return(
            <div
            style={{                            
            backgroundColor: "#f4f4f4",
            padding: "15px",
            marginTop: "20px",
            border: "1px solid #ccc",
            borderRadius: "5px",
            whiteSpace: "pre-wrap",
            fontFamily: "monospace",
              }}
            >
            <h3>Generated JSON:</h3>
            <textarea
            value={generatedJSON}
            readOnly
            style={{ width: "100%", height: "150px", marginTop: "10px" }}
            />
            <br />
            <Button type="button" onClick={onCopy} style={{ backgroundColor: "blue",color: "white" }}
>
                Copy to Clipboard
            </Button>              
            {copyStatus && <span style={{ marginLeft: "10px" }}>{copyStatus}</span>}
        </div>
    )}
            

