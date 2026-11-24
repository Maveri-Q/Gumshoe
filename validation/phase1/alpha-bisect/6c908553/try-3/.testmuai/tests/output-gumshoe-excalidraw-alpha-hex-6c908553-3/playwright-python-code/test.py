import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="c268b3ee-ada5-47ef-b1e8-394eda4754f5",
    name="Change Canvas Background Color via Hex Code",
    tc_id="TC-176",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"ready": "yes"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='51cc21e0-ae8f-4943-957c-e689b9d85600'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the three-lines button at the top left', instruction_id='e23316f4-9065-46e5-ab72-66a09cc253a6'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()
    
    async with testmu.step('Clicking the last colour square on the right under Canvas background', instruction_id='b27e4486-d130-4495-80b0-b5df3df84d40'):
        _loc_2 = page.locator("internal:role=button[name=\"Canvas background\"i]")
        
        await _loc_2.click()
    
    async with testmu.step('Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.', instruction_id='b916cb8e-a412-43be-8004-3c61f5a2c010'):
        set_var('ready', await testmu.vision_query(page, "Whether a colour picker with a Hex code text box is open is stored as {{ready}} exactly as yes or no.", ""))
    
    async with testmu.step('Waiting for Canvas background to be queued', instruction_id='04f5faed-79cd-43b3-8bf7-0da9a8086385'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Type "ff000080" into "Canvas background"', instruction_id='a76c3915-c509-45b9-8971-6340c1127fe3'):
        element_0 = page.locator("internal:role=textbox[name=\"Canvas background\"i]")
        
        await testmu.fill(element_0, "ff000080")
    
    async with testmu.step('Press Tab', instruction_id='0acef942-5c27-4f63-ac03-1556d4507ae7'):
        await page.wait_for_timeout(500)
        await page.keyboard.press('Tab')
    
    async with testmu.step('Waiting 2 seconds after pressing Tab', instruction_id='ddf7774b-3c3e-482d-af5e-e96cf86c8b07'):
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    testmu.run(test)