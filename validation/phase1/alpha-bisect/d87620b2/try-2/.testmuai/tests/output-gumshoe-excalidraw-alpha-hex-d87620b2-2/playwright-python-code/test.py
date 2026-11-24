import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="afad6b23-72cb-43f7-9d07-14b2bcbf7708",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-173",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='cf35fd22-cd2b-4c51-bb14-0ab3459cdcfb'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='cbe03a68-7946-41a4-b694-33ab9c6268d1'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last colour square on the right after the divider', instruction_id='2396648d-1526-44cd-8653-c995d5276cd8'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker with Hex code input is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {115: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(115).textContent.includes(\'Hex code\') && !!el(115).querySelector(\'input, textarea, [role="textbox"]\')) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Waiting for the next action in the queued plan', instruction_id='a6e4e379-ecc1-4a1e-8da4-d85389545cb5'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='bfd23023-418f-4c85-824c-6ed1fd31ae07'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='91d16470-6b10-42a9-b862-972be6d7f28a'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting for 2 seconds', instruction_id='18252903-499e-46fe-bfcd-20fd683e0ab3'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)