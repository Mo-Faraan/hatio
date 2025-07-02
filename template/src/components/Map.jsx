import { useState, useEffect } from "react";
import Button from "./Button";

export default function Map({ result, reset, initialInput }) {
    // Compose initial inputs: first is Default, rest are key-value
    const getInitialInputs = () => {
        if (Array.isArray(initialInput) && initialInput.length > 0) {
            // If first element is Default, use its 
            let defaultVal = "";
            let rest = [];
            if (initialInput[0]?.key === "Default") {
                defaultVal = initialInput[0].value;
                rest = initialInput.slice(1);
            } else {
                rest = initialInput;
            }
            return [{ key: "Default", value: defaultVal }, ...rest];
        }
        return [{ key: "Default", value: "" }, { key: "", value: "" }];
    };

    const [inputs, setInputs] = useState(getInitialInputs());

    useEffect(() => {
        setInputs([{ key: "Default", value: "" }, { key: "", value: "" }]);
    }, [reset]);

    useEffect(() => {
        setInputs(getInitialInputs());
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [initialInput]);

    function handleInputChange(index, field, event) {
        const newInputs = [...inputs];
        newInputs[index][field] = event.target.value;
        setInputs(newInputs);
    }

    function handleClick() {
        setInputs([...inputs, { key: "", value: "" }]);
    }

    result(inputs);

    return (
        <>
            <label>Mappings: </label>
            <br />
            <div>
                <input value="Default" disabled />
                <label> : </label>
                <input
                    placeholder="Enter default mapping for all other values"
                    value={inputs[0].value}
                    onChange={e => handleInputChange(0, "value", e)}
                />
            </div>
            <br />
            {inputs.slice(1).map((input, idx) => (
                <div key={idx + 1}>
                    <input
                        type="text"
                        placeholder="Enter the Key value : "
                        value={input.key}
                        onChange={e => handleInputChange(idx + 1, "key", e)}
                    />
                    <label> : </label>
                    <input
                        type="text"
                        placeholder="Enter value to be replaced : "
                        value={input.value}
                        onChange={e => handleInputChange(idx + 1, "value", e)}
                    />
                    <br />
                </div>
            ))}
            <Button type="button" onClick={handleClick}>ADD</Button>
        </>
    );
}