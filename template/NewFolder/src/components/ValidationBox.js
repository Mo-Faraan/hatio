import Button from "./Button";

export default function ValidationBox({inputValue,onValidate,onValidateChange,message}){
    return(
        <div>
            <h3>Enter JSON</h3>
            <div>
            <textarea
              style={{ width: '500px', height: '300px' }}
              placeholder='Paste JSON array like [{"name":"abc"},{"name":"xyz"}]'              
                value={inputValue}
              onChange={onValidateChange}
            />
            <br />
            <Button type="button" onClick={onValidate} style={{ marginTop: '10px' }}>
              Validate
            </Button>
            <p>{message}</p>
            </div>
        </div>
    )
}