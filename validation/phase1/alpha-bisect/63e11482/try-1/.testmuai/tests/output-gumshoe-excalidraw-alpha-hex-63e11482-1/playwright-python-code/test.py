import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="bfd90493-cd25-470e-a77a-fa6b1ef3b889",
    name="Set Canvas Background Color via Hex Code",
    tc_id="TC-177",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='3e8c0464-b610-44b2-ac14-9cbda8c1a27f'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button', instruction_id='8f3b464b-9ec5-4cdc-840e-c03d5eaa58a3'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last right-side color square after the thin divider', instruction_id='5da51b56-1828-4632-8359-d9450721e900'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the color picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(116).querySelector(\'input[aria-label="Canvas background"]\') && /Hex code/.test(el(116).innerText) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open color picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "a colour picker with a Hex code text box is open" is true right now is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Waiting for the plan steps to complete', instruction_id='8f309894-4386-412f-8806-4b5ba9988cd3'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='f4a4397d-72b1-40d9-8953-64ff41ca661c'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='3e069176-6b7a-4a83-ba02-2901646a1474'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds after tabbing out of the Hex code textbox', instruction_id='da98b273-aa46-468f-9bfc-931a1f2fe6c0'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)