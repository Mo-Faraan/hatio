export default function Template({selectedTemplate,onTemplateChange}){
    return(
    <>
    Select the Template:
          <label><input
            type="radio"
            name="template" 
            value="template1" 
            checked={selectedTemplate==="template1"}
            onChange={onTemplateChange} />
            Template1
          </label>
          <label style={{ marginLeft: "10px" }}>
            <input
            type="radio"
            name="template"
            value="template2"
            checked={selectedTemplate==="template2"}
            onChange={onTemplateChange}/>
            Template2
          </label>
          <br /><br />
    </>)
}