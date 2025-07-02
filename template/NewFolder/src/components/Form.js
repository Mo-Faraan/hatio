import { useState, useEffect, useMemo } from "react";
import CreatableSelect from "react-select/creatable";
import { dateArray, amountArray, dateFormat, template1, template2 } from "./Options";
import Select from "react-select";
import Template from "./Template";
import ValidationBox from "./ValidationBox";
import Generated from "./Generated";
import SubmitList from "./SubmitList";
import Button from "./Button";

export default function Form() {
  const [order, setOrder] = useState(1);
  const [editingIndex, setEditingIndex] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [generatedJSON, setGeneratedJSON] = useState({ pretty: "", string: "" });
  const [copyStatus, setCopyStatus] = useState("");
  const [submit, setSubmit] = useState([]);
  const [showGenerated, setShowGenerated] = useState(false);
  const [message, setMessage] = useState("");
  const [showValidation, setShowValidation] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState("template1");
  const [pastedIndexes, setPastedIndexes] = useState(new Set());
  const [logicalErrors, setLogicalErrors] = useState([]);

  const [form, setForm] = useState({
    isCustom: false,
    columnName: "",
    headerName: "",
    orderId: "",
    defaultValue: "",
    amountFormat: "paisa",
    dateFormat: "",
    map: "",
  });

  const getOptions = useMemo(() => {
    switch (selectedTemplate) {
      case "template1":
        return template1;
      case "template2":
        return template2;
      default:
        return [];
    }
  }, [selectedTemplate]);

  const notInAnyArray = !amountArray.includes(form.columnName) && !dateArray.includes(form.columnName);
  const disableAmount = form.isCustom === false && amountArray.includes(form.columnName) && !notInAnyArray;
  const disableDate = form.isCustom === false && dateArray.includes(form.columnName) && !notInAnyArray;

  const handleTemplateChange = (e) => {
    const newTemplate = e.target.value;
    if (submit.length > 0) {
      const confirmChange = window.confirm("Switching template will remove all the fields. Do you want to continue?");
      if (!confirmChange) return;
      setSubmit([]);
      setOrder(1);
      setForm({
        isCustom: false,
        columnName: "",
        headerName: "",
        orderId: "",
        defaultValue: "",
        amountFormat: "paisa",
        dateFormat: "",
        map: "",
      });
      setEditingIndex(null);
      setInputValue("");
    }
    setSelectedTemplate(newTemplate);
  };

  const validateJson = () => {
    try {
      const parsed = JSON.parse(inputValue);
      if (!Array.isArray(parsed)) throw new Error("Input must be a JSON array of objects");

      const normalizeBoolean = (value) => {
        if (typeof value === "boolean") return value;
        if (typeof value === "string") return value.toLowerCase() === "true";
        return false;
      };

      const normalised = parsed.map((item) => ({ ...item, isCustom: normalizeBoolean(item.isCustom) }));

      const duplicate = new Set();
      const getDuplicateWithoutOrderId = (obj) => {
        const { orderId, ...rest } = obj;
        const sorted = Object.keys(rest).sort().reduce((acc, key) => {
          acc[key] = rest[key];
          return acc;
        }, {});
        return JSON.stringify(sorted);
      };

      const parsedJson = normalised.filter((obj) => {
        const key = getDuplicateWithoutOrderId(obj);
        if (duplicate.has(key)) return false;
        duplicate.add(key);
        return true;
      });

      const currentTemplate = selectedTemplate === "template1" ? template1 : template2;
      const otherTemplate = selectedTemplate === "template1" ? template2 : template1;

      const currentColumn = currentTemplate.map((opt) => opt.value);
      const otherColumn = otherTemplate.map((opt) => opt.value);
      const allColumn = [...new Set([...currentColumn, ...otherColumn])];

      const error = [];
      for (let i = 0; i < parsed.length; i++) {
        const item = parsed[i];
        const col = (item.columnName || "").trim();
        const isCustom = item.isCustom === true;

        if (isCustom) {
          if (col === "") continue;
          if (allColumn.includes(col)) {
            error.push({ index: i, message: `Invalid: isCustom is true but columnName "${col}" is in template` });
          } else {
            error.push({ index: i, message: `Invalid: isCustom is true with columnName "${col}"` });
          }
          continue;
        }

        if (col === "") {
          error.push({ index: i, message: `Invalid: columnName is empty while isCustom is false` });
          continue;
        }

        if (otherColumn.includes(col)) {
          error.push({ index: i, message: `Invalid: columnName "${col}" doesn't belong to selected template` });
        }
      }

      const reordered = reassignOrderIds(parsed);
      setSubmit(reordered);
      setPastedIndexes(new Set(reordered.map((_, index) => index)));
      setGeneratedJSON(parsedJson);
      setLogicalErrors(error);
      setMessage("JSON validated with " + error.length + " logical error(s).")
      setInputValue("");
    } catch (e) {
      setGeneratedJSON([]);
      setMessage(e.message || 'Invalid JSON! Must be a JSON array.');
      setSubmit([]);
      setLogicalErrors([]);
    }
  };

  const selectedOption = useMemo(() => {
    const found = getOptions.find((opt) => opt.value === form.columnName);
    return found || (form.columnName ? { label: form.columnName, value: form.columnName } : null);
  }, [form.columnName, getOptions]);

  const selectedDateOption = useMemo(() => {
    return dateFormat.find((opt) => opt.value === form.dateFormat);
  }, [form.dateFormat]);

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      if (!inputValue.trim()) return;
      setForm((prev) => ({ ...prev, columnName: inputValue.trim() }));
      setInputValue("");
      event.target.blur();
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "isCustom") {
      const boolValue = value === "true";
      setForm((prev) => ({
        ...prev,
        isCustom: boolValue,
        defaultValue: boolValue ? prev.defaultValue : "",
      }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const reassignOrderIds = (items) => {
    return items.map((item, index) => ({ ...item, orderId: index + 1 }));
  };

  const handleSelectChange = (selectedOption) => {
    setForm((prev) => ({ ...prev, columnName: selectedOption.value }));
  };

  const alertUser = (e) => {
    e.preventDefault();
    e.returnValue = "";
  };

  useEffect(() => {
    window.addEventListener("beforeunload", alertUser);
    return () => {
      window.removeEventListener("beforeunload", alertUser);
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    let hName = form.headerName;
    if (hName === "") {
      hName = form.columnName.replaceAll("_", " ");
    }
    const formWithOrder = { ...form, headerName: hName, orderId: Number(order) };
    setOrder(order + 1);

    if (formWithOrder.amountFormat.toLowerCase() === "paisa") delete formWithOrder.amountFormat;
    if (!formWithOrder.map?.trim()) delete formWithOrder.map;
    if (!formWithOrder.dateFormat?.trim()) delete formWithOrder.dateFormat;
    if (form.isCustom === true) formWithOrder.columnName = "";
    else formWithOrder.defaultValue = "";

    if (!form.isCustom && !form.columnName.trim()) {
      alert("Please Enter the column name");
      return;
    }

    if (editingIndex !== null) {
      const updated = [...submit];
      updated[editingIndex] = formWithOrder;
      const reordered = reassignOrderIds(updated);
      setSubmit(reordered);
      const cleanedErrors = logicalErrors.filter(err => err.index !== editingIndex);
      setLogicalErrors(cleanedErrors);
      setEditingIndex(null);
    } else {
      setSubmit((prev) => [...prev, formWithOrder]);
    }

    setForm({
      isCustom: false,
      columnName: "",
      headerName: "",
      orderId: "",
      defaultValue: "",
      amountFormat: "paisa",
      dateFormat: "",
      map: "",
    });
  };

  return (

    <div>
      
    <div className="flex pt-5 pl-5 pb-6  border border-black-800 mt-0 ">
   
    <img class=" h-20 w-15  rounded-lg" src="/images/obj4.jpeg"  alt="" />
    <div>
    <h1 className="block font-bold  font-sans md:font-mono text-center text-lg">Welcome to Recon 2.0 Report Template Generation </h1>
     <p className="pt-3 pr-5 text-space-5 pl-5 font-serif ">Templates in Recon 2.0 are basically an array of objects represented in the JSON format and consists of collections of multiple key - value pairs. 
      These templates are stored in the RECON_REPORT_TEMPLATE table under the HEADER_JSON column. 
      Each object in the JSON data format contains keys which corresponds to the columns of 2 main tables: 
      Recon_Transaction_Master And Recon_Commission_Master </p>

    </div>
    </div>


    <form onSubmit={handleSubmit} className="w-full bg-back-image font-serif ">
      <div className="flex flex-col lg:flex-row gap-6 w-full px-6 pt-2">

      <div className="w-full md:w-1/3  space-y-4  rounded-md border-2 px-2 py-2">
        <Template selectedTemplate={selectedTemplate} onTemplateChange={handleTemplateChange} />

        <div>
          <label>Is Custom:</label>
          <div className="space-x-2 ">
            <label><input type="radio" name="isCustom" value="true" checked={form.isCustom === true} onChange={handleChange} /> True</label>
            <label><input type="radio" name="isCustom" value="false" checked={form.isCustom === false} onChange={handleChange} /> False</label>
          </div>
        </div>

        <div>
          <label>Column Name:</label>
          <CreatableSelect options={getOptions} placeholder="Select Column" onChange={handleSelectChange} isSearchable isDisabled={form.isCustom} value={selectedOption} onKeyDown={handleKeyDown} />
        </div>

        <div>
          <label>Header Name:</label>
          <input className="w-full p-2 border rounded"  name="headerName" value={form.headerName} onChange={handleChange} />
        </div>

        <div>
          <label>Default Value:</label>
          <input className="w-full p-2 border rounded" name="defaultValue" value={form.defaultValue} onChange={handleChange} disabled={!form.isCustom} />
        </div>

        <div>
          <label>Amount Format:</label>
          <div className="space-x-4">
            <label><input type="radio" name="amountFormat" value="paisa" checked={form.amountFormat === "paisa"} onChange={handleChange} disabled={disableAmount} /> Paisa</label>
            <label><input type="radio" name="amountFormat" value="rs" checked={form.amountFormat === "rs"} onChange={handleChange} disabled={disableAmount} /> Rupee</label>
          </div>
        </div>

        <div>
          <label>Date Format:</label>
          <Select options={dateFormat} placeholder="Select Date" isSearchable isDisabled={disableDate} value={selectedDateOption} onChange={(opt) => setForm((prev) => ({ ...prev, dateFormat: opt?.value || "" }))} />
        </div>

        <div>
          <label>Map:</label>
          <input  className="w-full p-2 border rounded" name="map" value={form.map} onChange={handleChange} />
        </div>

        <div className="flex items-center gap-3">
          <Button type="submit" className={`w-40 h-10 rounded-md bg-blue-900 hover:bg-blue-900 text-white`}>{editingIndex !== null ? "Update" : `Add (${submit.length})`}</Button>
          {editingIndex !== null && (
            <Button type="button" onClick={() => {
              setForm({ isCustom: false, columnName: "", headerName: "", orderId: "", defaultValue: "", amountFormat: "paisa", dateFormat: "", map: "" });
              setEditingIndex(null);
              setInputValue("");
            }} className={`px-4 py-1 bg-white border-2 border-blue-800 text-blue-800 rounded hover:bg-slate-400 `}>Cancel</Button>
          )}

          
        <Button type="button" onClick={() => setShowValidation((prev) => !prev)} className={`w-60 h-10 rounded-md bg-blue-900 hover:bg-blue-900 text-white`}>
          {showValidation ? "Hide Validation Box" : "Show Validation Box"}
        </Button>
        </div>
      </div>
      

      <div className="w-full md:w-1/3 space-y-4 rounded-md border-2 px-2 py-2">
        <h3 className="text-lg font-bold">Added Items: </h3>
        
        {logicalErrors.length > 0 && (
          <div className="bg-red-100 border border-red-500 p-3 rounded">
            <h4 className="font-bold">Logical Errors ({logicalErrors.length})</h4>
            <ul className="list-disc ml-4">
              {logicalErrors.map((err, idx) => (
                <li key={idx}>Row {err.index + 1}: {err.message}</li>
              ))}
            </ul>
          </div>
        )}

        <SubmitList
          items={submit}
          pastedIndexes={pastedIndexes}
          invalidIndexes={new Set(logicalErrors.map((err) => err.index))}
          logicalErrors={logicalErrors}
          onEdit={(index) => {
            const item = submit[index];
            setForm({
              isCustom: item.defaultValue !== undefined && item.defaultValue !== "",
              columnName: item.columnName || "",
              headerName: item.headerName || "",
              orderId: item.orderId || "",
              defaultValue: item.defaultValue || "",
              amountFormat: item.amountFormat || "paisa",
              dateFormat: item.dateFormat || "",
              map: item.map || "",
            });
            setEditingIndex(index);
            setInputValue("");
          }}
          onDelete={(index) => {
            const confirmDelete = window.confirm("Are you sure you want to delete this item?");
            if (confirmDelete) {
              const updatedList = [...submit];
              updatedList.splice(index, 1);
              setSubmit(reassignOrderIds(updatedList));
              if (editingIndex === index) {
                setForm({ isCustom: false, columnName: "", headerName: "", orderId: "", defaultValue: "", amountFormat: "paisa", dateFormat: "", map: "" });
                setEditingIndex(null);
                setInputValue("");
              }
            }
          }}
        />
      </div>
      <div className="w-1/3 space-y-4  border-2 rounded-md px-2 py-2">
       <Button type="button" className="w-40 h-10 rounded-md bg-blue-800 hover:bg-blue-900 text-white " onClick={() => {
          const sorted = [...submit].sort((a, b) => a.orderId - b.orderId);
          setGeneratedJSON({ pretty: JSON.stringify(sorted, null, 2), string: JSON.stringify(sorted) });
          setShowGenerated(true);
        }}>Generate</Button>
           {showValidation && (
          <ValidationBox onValidate={validateJson} onValidateChange={(e) => setInputValue(e.target.value)} inputValue={inputValue} message={message} />
        )}

      
      
        {showGenerated && (
          <Generated generatedJSON={generatedJSON.string} copyStatus={copyStatus} onCopy={async () => {
            try {
              await navigator.clipboard.writeText(generatedJSON.string);
              setCopyStatus("Copied!");
              setTimeout(() => setCopyStatus(""), 2000);
            } catch {
              setCopyStatus("Failed to copy");
            }
          }} />
        )}
        </div>
        </div>
      
    </form>
    </div>
    
  );
}
