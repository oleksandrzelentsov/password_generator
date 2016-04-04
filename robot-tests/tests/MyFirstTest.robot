*** Settings ***
Documentation  This is my first test

*** Variables ***

${comparison_results}
${generated_password}

*** Test Cases ***
Check if 3 is less than 4
    [Documentation]  Is 3 less than 4?
    [Tags]  Smoke
    ${comparison_results} =  evaluate  "3 < 4"
    should be true  ${comparison_results}


Password length is correct
    [Documentation]  Check if password generation returns data with correct length
    [Tags]  Smoke
    ${generated_password} =  evaluate  "myModule.generate_password(30)"  modules=myModule
    length should be  ${generated_password}  30



*** Keywords ***