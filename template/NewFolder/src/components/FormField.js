import React from "react";
import options1 from "./Options";
import CustomCreatable from "./CustomCreatableSelect";


export default function FormField({
  form,
  inputValue,
  setInputValue,
  onChange,
  onSelectChange,
  onKeyDown,
  disableAmount,
  disableDate,
}) {
//   const selectedOption = options1.find(opt => opt.value === form.columnName) || 
//     (form.columnName ? { label: form.columnName, value: form.columnName } : null);

  return (
    <>
      <div>
        Is Custom:
        <label>
          <input
            type="radio"
            name="isCustom"
            value="true"
            checked={form.isCustom === true}
            onChange={onChange}
          />
          True
        </label>
        <label style={{ marginLeft: "10px" }}>
          <input
            type="radio"
            name="isCustom"
            value="false"
            checked={form.isCustom === false}
            onChange={onChange}
          />
          False
        </label>
      </div>
      <br />
      <div>
        Column Name:
        <CustomCreatable
        value={form.columnName}
        onChange={(val) => onSelectChange({ value: val })}
        options1={options1}
        />
      </div>

      <br />

      <div>
        Header Name:
        <input
          name="headerName"
          value={form.headerName}
          placeholder="Header Name"
          onChange={onChange}
        />
      </div>

      <br />

      <div>
        Default Value:
        <input
          name="defaultValue"
          value={form.defaultValue}
          placeholder="Default Value"
          onChange={onChange}
          disabled={!form.isCustom}
        />
      </div>

      <br />

      <div>
        Amount Format:
        <label>
          <input
            type="radio"
            name="amountFormat"
            value="paisa"
            checked={form.amountFormat === "paisa"}
            onChange={onChange}
            disabled={disableAmount}
          />
          Paisa
        </label>
        <label style={{ marginLeft: "10px" }}>
          <input
            type="radio"
            name="amountFormat"
            value="rs"
            checked={form.amountFormat === "rs"}
            onChange={onChange}
            disabled={disableAmount}
          />
          Rupee
        </label>
      </div>

      <br />

      <div>
        Date Format:
        <input
          name="dateFormat"
          value={form.dateFormat}
          placeholder="Date Format"
          onChange={onChange}
          disabled={disableDate}
        />
      </div>

      <br />

      <div>
        Map:
        <input
          name="map"
          value={form.map}
          placeholder="Map"
          onChange={onChange}
        />
      </div>

      <br />
    </>
  );
}
