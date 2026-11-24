import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="fcaf59e2-5abf-409b-8020-aa04c0cee3ee",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-163",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='9f6bd9e1-679e-442f-af7c-f142497118a1'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu three-lines button at the top left', instruction_id='c325aa4b-b105-4908-b6cd-13f88b7afb50'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last right colour square after the thin divider', instruction_id='51f01853-1f12-4430-973a-c6bac2012355'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {109: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(109).querySelector(\'input, [role="textbox"]\') && /Hex code/i.test(el(109).innerText)) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Waiting for the next steps to load', instruction_id='2b9fb190-ad0f-489b-a02e-c21a4015470c'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='42be0478-ebb8-4df2-8c58-dea9bb6b5ea0'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='316c449c-669e-4a70-9dd0-39b6a1ae7aec'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='95e6436c-0708-4313-b6c0-b5a77d26e9d3'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)