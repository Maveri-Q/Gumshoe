import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="7761785b-965b-45eb-bb66-745b07b10089",
    name="Set Canvas Background Color Using Hex Code",
    tc_id="TC-166",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='28916bb1-52e4-44ef-8daa-29f24c1ce726'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the main menu button in the top-left header', instruction_id='f54dfaca-b2ea-4b0f-8ba2-7a2f1155fbab'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last Canvas background color square on the right', instruction_id='9b4276af-2496-4c77-b90c-6fcb20d61ca7'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Checking whether the colour picker is open'):
        set_var('ready', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {109: 0, 110: 1};\n  const el = (i) => els[__m[i]];\n  const __v = ((/Hex code/i.test(el(109).textContent || '') && el(109).getClientRects().length > 0 && typeof el(110).value === 'string') ? 'yes' : 'no');\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['internal:role=dialog >> internal:has-text="Hex code#"i', 'internal:role=textbox[name="Canvas background"i]'], query='whether a colour picker dialog with a Hex code text box is open', expected_value='', needs_unit_conversion=False, operator='equals', transforms=['strip'], condition='Whether "a colour picker with a Hex code text box is open" is true right now is stored as {{ready}} exactly as yes or no.'))
    
    async with testmu.step('Typing ff000080 into Hex code text box', instruction_id='52b1eccf-bd77-4319-ba2f-6596a220fa42'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Pressing Tab key', instruction_id='9220e682-21ea-4cfb-b325-7723b64600bc'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds after pressing Tab', instruction_id='e7c178cb-8efd-43f8-a0e1-379c20a0d794'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)