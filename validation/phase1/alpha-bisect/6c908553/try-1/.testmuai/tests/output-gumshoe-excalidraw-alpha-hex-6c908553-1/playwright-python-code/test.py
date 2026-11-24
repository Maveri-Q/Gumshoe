import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="c5153c9a-8985-41a4-866f-7208b01ece96",
    name="Change Canvas Background Color via Hex Input",
    tc_id="TC-174",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='fbe6f4dd-d01a-43d4-b41e-47d6a5d51ce1'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button', instruction_id='5cfe04ae-2211-475f-bd25-ceb0fb74ba4b'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last colour square on the right in the Canvas background menu', instruction_id='0427b1d8-2a20-4e11-a99f-d6ee6e61f802'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the color picker Hex code box is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {115: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(115).querySelector(\'input[aria-label="Canvas background"]\') ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open color picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored exactly as yes or no as {{ready}}.'))
    
    async with testmu.step('Waiting for the plan to queue', instruction_id='48c303d1-a6e4-49dc-ace1-5b1bccdb8f25'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Press Ctrl+A', instruction_id='91ca63d7-211e-4a3a-b3e6-790dd0345e5a'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('ControlOrMeta+A')
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='8829c48d-7e14-41fa-accd-89e701bf2aff'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='48c90102-bf78-45b1-adc2-82a1e1e311ce'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2000 ms after updating the Hex code text box', instruction_id='53a999b9-0cab-4739-a37e-2e303a2d9e44'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)