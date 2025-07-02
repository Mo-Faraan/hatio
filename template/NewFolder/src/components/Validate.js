import { useState } from 'react';
import CancelButton from './Cancel';
import EditButton from './Edit';
import DeleteButton from './Delete';
import CopyButton from './Copy';

export default function Validate() {
  const [input, setInput] = useState('');
  const [parsedJson, setParsedJson] = useState([]);
  const [message, setMessage] = useState('');
  const [editingIndex, setEditingIndex] = useState(null);
  const [editContent, setEditContent] = useState('');

  const validateJson = () => {
    try {
      const parsed = JSON.parse(input);
      if (!Array.isArray(parsed)) throw new Error('Input must be a JSON array of objects');
      setParsedJson(parsed);
      setMessage('Valid JSON');
    } catch (e) {
      setParsedJson([]);
      setMessage('Invalid JSON! Must be a JSON array.');
    }
  };

  const startEditing = (index) => {
    setEditingIndex(index);
    setEditContent(JSON.stringify(parsedJson[index], null, 2));
  };

  const saveEdit = () => {
    try {
      const updated = JSON.parse(editContent);
      const newList = [...parsedJson];
      newList[editingIndex] = updated;
      setParsedJson(newList);
      setEditingIndex(null);
      setEditContent('');
      setMessage('Item updated');
    } catch (e) {
      setMessage('Invalid JSON in edit area');
    }
  };

 

  const handleDelete = (index) => {
    const filtered = parsedJson.filter((_, i) => i !== index);
    setParsedJson(filtered);
    setMessage('Item deleted');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>JSON Validator & Formatter</h2>
      <p>{message}</p>

      <div style={{ display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <h3>Enter JSON</h3>
          <textarea
            style={{ width: '500px', height: '300px' }}
            placeholder='Paste JSON array like [{"name":"abc"},{"name":"xyz"}]'
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <br />
          <button onClick={validateJson} style={{ marginTop: '10px' }}>
            Validate
          </button>
        </div>

        <div style={{ flex: 1 }}>
          <h3>Added Items:</h3>
          <ul style={{ listStyle: "none", padding: 2 }}>
            {parsedJson.map((item, idx) => (
              <li
                key={idx}
                style={{
                  background: "#f0f0f0",
                  padding: "10px",
                  marginBottom: "10px",
                  borderRadius: "5px",
                  fontFamily: "monospace",
                }}
              >
                {editingIndex === idx ? (
                  <>
                    <textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      style={{ width: "100%", height: "150px", fontFamily: "monospace" }}
                    />
                    <br />
                    <button onClick={saveEdit} style={{ marginRight: "10px" }}> Save</button>
                    <CancelButton cancelEdit = {() => {
                        setEditingIndex(null);
                        setEditContent('');
                    }}
                    />
                  </>
                ) : (
                  <>
                    <pre>{JSON.stringify(item, null, 2)}</pre>
                    <EditButton onEdit={() => startEditing(idx)} style={{ marginRight: "10px" }}/>                   
                    <DeleteButton onDelete={() => handleDelete(idx)} style={{ backgroundColor: "#e74c3c", color: "white" }}/>
                   </>
                )}
              </li>
            ))}
          </ul>
          {parsedJson.length > 0 && (
    <div style={{ marginTop: '30px' }}>
        <h3>Final JSON</h3>
        <pre style={{ background: '#f4f4f4', padding: '15px', borderRadius: '5px' }}>
        {JSON.stringify(parsedJson)}
        </pre>
 <div
              style={{
                marginTop: "20px",
                backgroundColor: "#f4f4f4",
                padding: "15px",
                border: "1px solid #ccc",
                borderRadius: "5px",
                whiteSpace: "pre-wrap",
                fontFamily: "monospace", 
              }}
            >
              <textarea
                value={JSON.stringify(parsedJson)}

                readOnly
                style={{ width: "100%", height: "150px", marginTop: "10px" }}
              />
              <br />
              <CopyButton text= {JSON.stringify(parsedJson)}/>
                {/* onCopyStatus={setCopyStatus}  */}
              {/* {copyStatus && <span style={{ marginLeft: 10 }}>{copyStatus}</span>} */}
              </div>

            </div>
          )}
          </div>
          </div>
        </div>
)};
