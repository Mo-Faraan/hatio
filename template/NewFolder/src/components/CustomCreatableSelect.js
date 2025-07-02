import { useState, useEffect } from "react";


export default function CustomCreatable({ options1, value, onChange }) {
  const [input, setInput] = useState(value || "");
  const [showDropDown, setShowDropDown] = useState(false);


  useEffect(() => {
    setInput(value || "");
  }, [value]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const match = options1.find(
        (opt) => opt.toLowerCase() === input.toLowerCase()
      );
      if (match) {
        onChange(match);
        setShowDropDown(false);
      }
    }
  };

  const handleSelect = (val) => {
    setInput(val);
    onChange(val);
    setShowDropDown(false);
  };

  
  const filtered = options1.filter((opt) =>
    opt.toLowerCase().includes(input.toLowerCase())
  );


  return (
    <div style={{ width: "100%", position: "relative" }}>
      <input
        value={input}
        onChange={(e) => {
          setInput(e.target.value);
          setShowDropDown(true);
        }}
        onKeyDown={handleKeyDown}
        placeholder="Type or select"
        style={{
          width: "100%",
          padding: "6px 30px 6px 8px",
          boxSizing: "border-box",
        }}
      />

      <button
        type="button"
        onClick={() => setShowDropDown((prev) => !prev)}
        style={{
          position: "absolute",
          right: "5px",
          top: "20%",
          border: "none",
          background: "transparent",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        ▼
      </button>

      {showDropDown && (
        <ul
          style={{
            position: "absolute",
            width: "100%",
            background: "white",
            border: "1px solid #ccc",
            margin: 0,
            padding: 0,
            listStyle: "none",
            maxHeight: "100px",
            overflowY: "auto",
            zIndex: 1,
          }}
        >
             {filtered.length > 0 ? (
            filtered.map((opt) => (
              <li
                key={opt}
                onClick={() => handleSelect(opt)}
                style={{ padding: "6px", cursor: "pointer" }}
              >
                {opt}
              </li>
            ))
          ) : (
            <li
              style={{
                padding: "6px",
                color: "gray",
                fontStyle: "italic",
                cursor: "default",
              }}
            >
              No matching option
            </li>
          )}
        </ul>
      )}
    </div>
  );
}
