import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="83663a4f-01d9-4d6e-86ba-7d5df409cd03",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-175",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='31118f5e-3099-4136-897f-22c5086277e7'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top left', instruction_id='9ef1839a-48b0-4fce-b22f-d70bf7a2154c'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last canvas background color swatch on the right side', instruction_id='881dcb9f-50c2-437f-96ef-5a2cebd9ac29'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Reading whether the color picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js='(els) => {\n  const __m = {115: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(115).querySelector(\'input[placeholder="Color"], input[aria-label="Canvas background"]\') && !!(el(115).offsetWidth || el(115).offsetHeight || el(115).getClientRects().length) ? \'yes\' : \'no\');\n  return (typeof __v === \'boolean\' ? String(__v) : __v);\n}', locators=['internal:role=dialog >> internal:has-text="Hex code#"i'], query='whether the open color picker dialog contains a visible Hex code text box', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether a colour picker with a Hex code text box is open is stored exactly yes or no as {{ready}}.'))
    
    async with testmu.step('Typing ff000080 into the hex code text box', instruction_id='a4573a18-e5a9-486e-abd4-a495f16ae6b0'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Pressing Tab key after entering the hex code', instruction_id='15b3213c-d44d-4ece-910a-93ff3752096b'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds after pressing Tab', instruction_id='e35abe0d-df4d-47a5-aebe-41176e3670c3'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)