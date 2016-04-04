*** Variables ***

${LIBS} =  ../libraries/

*** Settings ***
Documentation    Tests main file functions
#Library  Builtin
Library  Collections
Library  String
Library  ../libraries/MyLibrary.py

*** Test Cases ***
Password uniqueness
    [Documentation]  Generated passwords are unique
    ${a} =  Generate 10 Passwords Of Length 5
    log list  ${a}
    list should not contain duplicates  ${a}


*** Keywords ***

Generate Password Of Length ${length:\d+}
    [Documentation]  Generates one password with specified length.
    ${temp} =  evaluate  myModule.generate_password(${length})  modules=myModule
    [Return]  ${temp}


Generate Password Of Length ${length:\d+} With Seed ${seed:\d+}
    [Documentation]  Generates one password with specified length.
    ${temp} =  evaluate  myModule.generate_password(${length}, ${seed})  modules=myModule
    [Return]  ${temp}


Generate ${n:\d+} Passwords Of Length ${length:\d+}
    [Documentation]  Get list of randomly generated passwords.
    [Teardown]  sleep  1
    ${PASSWORDS} =  create list
    :FOR  ${index}  IN RANGE  0  ${n}
    \  ${temp} =  Generate Password Of Length ${length} With Seed ${index}
    \
    \  append to list  ${PASSWORDS}  ${temp}

    [Return]  ${PASSWORDS}