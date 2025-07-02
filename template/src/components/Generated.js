import Button from "./Button";

export default function Generated({generatedJSON,copyStatus,onCopy}) {
  return(
    <div className= "w-full lg:w-full space-y-4">
      <h3 className="text-lg font-semibold mb-2 w-full">Generated JSON:</h3>

      <textarea
      value={generatedJSON}
      readOnly
      className="w-full h-40 p-2 text-sm font-mono rounded border border-gray-300 resize-none"
      />
      <div className="mt-3">
        <Button type="button" onClick={onCopy}    
          className={`w-40 h-10 rounded-md bg-blue-800 hover:bg-blue-900 text-white`}>
        Copy to Clipboard
        </Button>              
        {copyStatus && <span  className="ml-3 text-sm">{copyStatus}</span>}
      </div>
    </div>
  )
}
            

