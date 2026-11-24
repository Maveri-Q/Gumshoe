import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="a615b103-3e64-4d00-b8d1-fc17aa384531",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-170",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='9267d80b-a2eb-456c-b60f-0d4b4cf8fe4c'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left corner', instruction_id='a8575ec5-4c83-429d-a8e1-c3e405c47056'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last color square in the Canvas background row', instruction_id='a5d84ba2-b754-4598-8cf7-226fc742f781'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {116: 0};\n  const el = (i) => els[__m[i]];\n  const __v = ((el(116).textContent.includes(\'Hex code\') && !!el(116).querySelector(\'input[placeholder="Color"]\') && !!(el(116).offsetWidth || el(116).offsetHeight || el(116).getClientRects().length)) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether an open colour picker dialog contains a Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='the answer to whether "a colour picker with a Hex code text box is open" is stored exactly as yes or no as {{ready}}'))
    
    async with testmu.step('Waiting for the next step to run', instruction_id='9db20753-9aee-49cf-85fa-e309d137c181'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='7c04f4bc-20cd-49ea-a627-3185cabfb806'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='1a4e06e3-59a1-4037-b184-089052254d7e'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2000 ms after pressing Tab', instruction_id='087b3b41-f26d-45af-b724-8560554f0c0c'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)