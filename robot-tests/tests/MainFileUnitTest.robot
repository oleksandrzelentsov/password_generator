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
    ${passwords} =  Generate 100 Passwords Of Length 2
    log list  ${passwords}
    list should not contain duplicates  ${passwords}


*** Keywords ***

Generate Password Of Length ${length:\d+}
    [Documentation]  Generates one password with specified length.
    ${password} =  evaluate  myModule.generate_password(${length})  modules=myModule
    [Return]  ${password}


Generate Password Of Length ${length:\d+} With Seed ${seed:\d+}
    [Documentation]  Generates one password with specified length.
    ${password} =  evaluate  myModule.generate_password(${length}, ${seed})  modules=myModule
    [Return]  ${password}


Generate ${n:\d+} Passwords Of Length ${length:\d+}
    [Documentation]  Get list of randomly generated passwords.
    [Teardown]  sleep  1
    ${passwords} =  create list
    :FOR  ${index}  IN RANGE  0  ${n}
    \  ${password} =  Generate Password Of Length ${length} With Seed ${index}
    \
    \  append to list  ${passwords}  ${password}

    [Return]  ${passwords}