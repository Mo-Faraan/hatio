import { useState } from "react";
import Button from "./Button";

export default function Map() {
    const [map, setMap] = useState(0);
    const [key, setKey] = useState();
    const [val, Setval] = useState();
    const [data, setData] = useState([]);
    // let p = <>
    //     <input type="text" value="default" unavailable></input>
    //     <label> : </label>
    //     <input type="text" value={value} placeholder="Enter the default value for all other keys :"></input>
    // </>

    let inputs = []
    
    let d =
    <><label>{data}</label></>
    for (let i=0; i<Number(map); i++){
        inputs.push(
            <div>
                <input
                        type="text"
                        placeholder="Enter the Key value : "
                        value={key}
                    />
                <label> : </label>
                <input
                        type="text"
                        placeholder="Enter the Key value : "
                        value={val}
                    />
                <label> : </label>
                {d}
            </div>
        )
    }

    
    function handleClick() {
        setMap((prev) => (prev+1));
        setData((prevData => ([ ...prevData, key, val])));
    }

    function handleChange(e){
        setKey(e.target.value);
        Setval(e.target.value);
    }
    
    return (
        <>
            <label>Mappings: </label>
            <br />
            {/* {(map) ? p : null} */}
            {inputs}
            
            <Button type="button" onClick={handleClick} onChange={handleChange} >ADD</Button>
        </>
    );
}



// import { useState } from "react";

// export default function Map() {
//     const [defaultVal, setDefaultVal] = useState(false);
//     const [inputs, setInputs] = useState([]);
//     let p = <>
//         <input type="text" value="default" unavailable></input>
//         <label> : </label>
//         <input type="text" placeholder="Enter the default value for all other keys :"></input>
//     </>
//     function handleInputChange(index, field, event) {
//         const newInputs = [...inputs];
//         newInputs[index][field] = event.target.value;
//         setInputs(newInputs);
//     }

//     function handleClick() {
//         setInputs([...inputs, { "" : "" }]);
//         setDefaultVal(true);
//     }

//     return (
//         <>
//             <label>Mappings: </label>
//             <br />
//             {inputs.map((input, idx) => (
//                 <div key={idx}>
//                     <input
//                         type="text"
//                         placeholder="Enter the Key value : "
//                         value={input.key}
//                         onChange={e => handleInputChange(idx, "key", e)}
//                     />
//                     <label> : </label>
//                     <input
//                         type="text"
//                         placeholder="Enter value to be replaced : "
//                         value={input.value}
//                         onChange={e => handleInputChange(idx, "value", e)}
//                     />
//                     <br />
//                 </div>
//             ))}
//             {defaultVal ? p : null} <br />
//             <button type="button" onClick={handleClick}>ADD</button>
//             <pre>{JSON.stringify(inputs, null, 2)}</pre>
//         </>
//     );
// }