
const temperature_form = document.getElementById("Temperature-form");
const errors = document.getElementById("errors");

const converter_page = document.getElementById("convert-page");
const result_page = document.getElementById("result-page");
const from_id = document.getElementById("from_id")
const result_id = document.getElementById("result_id")

function Convert(from,to,value){
    let result = "";
    if(from === "°C" && to === "°F" ){
        result =  (value * (9/5) + 32);
    }
    else if (from === "°F" && to === "°C" ){
        result = ((value - 32)* (9/5) );
    }
    else if (from === "K" && to === "°C" ){
        result = (value - 273.15 );
    }
    else if (from === "°C" && to === "K" ){
        result = (value + 273.15 );
    }
    else if (from === "°F" && to === "K" ){
        result = ((value - 32)* (9/5) ) + 273.15;
    }
    else if (from === "K" && to === "°F" ){
        result = ((value - 32)* (9/5) ) - 273.15;
    }
    return result;
}

temperature_form.addEventListener("submit",(e)=>{
    e.preventDefault()

    const unit_from = temperature_form.unit_from.value;
    const unit_to = temperature_form.unit_to.value;
    const temperature = temperature_form.temperature_value.value;

    console.log(`Convert from  ${temperature} ${unit_from} to ${unit_to}`)
    try{
        if(unit_to === unit_from){
            throw new Error("Units cannot be the same");
        }
        let result = Convert(unit_from,unit_to,temperature);
        console.log("Result: " + result);

        converter_page.style.display = "none";
        result_page.style.display = "block";
        from_id.innerText = `${temperature} ${unit_from}`;
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
