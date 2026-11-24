import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="c4e8a632-3ebc-485b-a2a9-36058ef3e845",
    name="Change Canvas Background Color Using Hex Code",
    tc_id="TC-160",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://127.0.0.1:4301/', instruction_id='1de494e0-3ab8-4825-af10-05a1c53e3d6a'):
        await page.goto("http://127.0.0.1:4301/")
    
    async with testmu.step('Clicking the three-line menu button in the top-left header', instruction_id='71c0aff0-9930-4e4d-bd81-a99a6f455140'):
        _loc_1 = page.locator("internal:testid=[data-testid=\"main-menu-trigger\"s]")
        
        await _loc_1.click()


if __name__ == "__main__":
    testmu.run(test)