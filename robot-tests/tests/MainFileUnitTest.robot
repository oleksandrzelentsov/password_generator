*** Settings ***
Documentation    Tests main file functions
Library  Collections

*** Test Cases ***
Get_args returns list
    [Tags]    Smoke
    should be true  "isinstance(main.get_args(), list)"  modules=${CURDIR}/../../main.py


*** Keywords ***