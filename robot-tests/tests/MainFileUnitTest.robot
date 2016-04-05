*** Variables ***

${LIBS} =  ../libraries/

*** Settings ***
Documentation    Tests main file functions
#Library  Builtin
Library  Collections
Library  String
Library  ${LIBS}PasswordGenerationLibrary.py

*** Test Cases ***

Password Uniqueness
    [Documentation]  Checks password uniqueness.
    Given Generate 10000 Passwords 5 Characters Long
    When The Passwords Are Generated
    Then Passwords Should Be Unique


*** Keywords ***

Passwords Should Be Unique
    [Documentation]  Checks if passwords generated are unique
    ${passwords} =  Generated Passwords
    list should not contain duplicates  ${passwords}

The Passwords Are Generated
    [Documentation]  Checks if passwords are generated
    ${passwords} =  Generated Passwords
    should not be empty  ${passwords}