export default function Template({selectedTemplate,onTemplateChange}){
    return(
    <div className=" text-md">
    <span className=" mt-4 mb-0.5">Select the Template:</span>
         <label className="mr-4">
            <input className="mr-1"
            type="radio"
            name="template" 
            value="template1" 
            checked={selectedTemplate==="template1"}
            onChange={onTemplateChange} />
            Template1
        </label>
        <label style={{ marginLeft: "10px" }}>
            <input className="mr-1"
            type="radio"
            name="template"
            value="template2"
            checked={selectedTemplate==="template2"}
            onChange={onTemplateChange}/>
            Template2
        </label>
   
    </div>
    
    )
}