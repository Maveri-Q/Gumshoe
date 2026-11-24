import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="6b5837f5-ec43-4d4d-bd18-c652359c2ab7",
    name="Set Canvas Background Color via Hex Code",
    tc_id="TC-159",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='63baa5b1-594a-49dd-9274-e5bebce37212'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button (three lines) in the top left header', instruction_id='1db331d2-a40c-4305-aff8-ca4d2d376d7d'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last canvas background colour square in the menu', instruction_id='42c88a0c-0d32-4279-a801-af71ac604eb5'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the color picker Hex field is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {115: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(115).querySelector(\'input, [role="textbox"]\') && /Hex code/i.test(el(115).innerText)) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open color picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Waiting for the queued plan to execute', instruction_id='212b141c-7a36-47e6-beba-84ee5921f715'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='5174d1de-bbc8-4179-b723-10bee3e2a3ad'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='61384ad3-3b21-4fc8-96a0-ed3fcd48e344'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2000 ms after pressing Tab', instruction_id='e161b10e-2a97-40df-a888-0be74250134d'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)