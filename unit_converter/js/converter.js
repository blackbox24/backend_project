const length_form  = document.getElementById("Length-form");

const len_units = ["µm","mm","cm","dc","m","dam","km","Mm"];

const errors = document.getElementById("errors");
const converter_page = document.getElementById("convert-page");
const result_page = document.getElementById("result-page");
const from_id = document.getElementById("from_id")
const result_id = document.getElementById("result_id")

function Convert(from,to,value){
    let from_index = 0;
    let to_index = 0;
    for(var i = 0; i < len_units.length; i++){
        if(len_units[i] === from){
            from_index = i;
            console.log(from_index)
        }
        else if(len_units[i] === to){
            to_index = i;
            console.log(to_index)
        }
    }
    if(from_index < to_index){
        return (10 ** (-to_index + from_index)) * value
    }
    else if(from_index > to_index){
        return  (10 ** (from_index - to_index)) * value
    }
    return 0;
}

length_form.addEventListener("submit",(e)=>{
    e.preventDefault()

    const unit_from = length_form.unit_from.value;
    const unit_to = length_form.unit_to.value;
    const length = length_form.length_value.value;

    console.log(`Convert from  ${length} ${unit_from} to ${unit_to}`)
    try{
        if(unit_to === unit_from){
            throw new Error("Units cannot be the same");
        }
        let result = Convert(unit_from,unit_to,length);
        console.log("Result: " + result);

        converter_page.style.display = "none";
        result_page.style.display = "block";
        from_id.innerText = `${length} ${unit_from}`;
        result_id.innerText = `${result}${unit_to}`;

    }catch(error){
        console.error(error)
        errors.innerText = "Units cannot be the same";
        errors.style.display = "block";
        errors.style.color = "red";

        setTimeout(()=>{
            errors.style.display = "none";
        },2000)
    }

})
