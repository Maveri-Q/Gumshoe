import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="bf133a86-66e6-4b84-b0a1-fcf3cce87351",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-171",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='1ed40cc7-c5f1-4e54-b093-459fd153d6a1'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button', instruction_id='2b434ead-efda-4ef8-bf5f-31bd2971c917'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last Canvas background color square on the far right', instruction_id='1989b652-908c-4356-a55c-f7692968f5b3'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Checking whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (!!el(116).querySelector(\'input[aria-label="Canvas background"]\') && /Hex code/i.test(el(116).innerText));\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether a colour picker with a Hex code text box is open', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Exactly yes or no is stored as {{ready}} for whether "a colour picker with a Hex code text box is open" is true right now.'))
    
    async with testmu.step('Waiting for the queued plan to start', instruction_id='e2b3c62f-1067-41cb-93dd-9cd20a41597d'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='7132e565-7639-4768-9587-d2979a9f8e20'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='189063b8-6411-4494-b3b2-a4359fa71784'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2000 milliseconds', instruction_id='45d8c701-0124-4c17-868f-4449e06a2b62'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)