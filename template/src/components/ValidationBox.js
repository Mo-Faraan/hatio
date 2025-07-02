import Button from "./Button";

export default function ValidationBox({inputValue,onValidate,onValidateChange,message}){
  return(
    <div className="w-full max-w-2xl mt-4">
      <h3 className="text-base font-semibold mb-2">Enter JSON</h3>            
      <textarea
      className="w-full h-72 p-3 text-sm font-mono border border-gray-300 rounded resize-y"
      placeholder='Paste JSON array like [{"name":"abc"},{"name":"xyz"}]'              
      value={inputValue}
      onChange={onValidateChange}
      />
      
      <Button type="button" onClick={onValidate}  className="w-40 h-10 rounded-md bg-blue-800 hover:bg-blue-900 text-white">
        Validate
      </Button>
      
      <p className="mt-2 text-sm text-gray-700">{message}</p>      
    </div>
  )
}