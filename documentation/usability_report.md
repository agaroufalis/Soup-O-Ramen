# Usability Report

## Persona Gallery

1. **The Nervous New Server**
   - Goal: Create a correct order quickly and avoid mistakes.
   - Pain Points: Unclear order state, confusing save vs submit behavior, fear of losing changes.

2. **The Busy Shift Lead**
   - Goal: Manage multiple orders simultaneously and keep the queue moving.
   - Pain Points: Hard-to-read order status, lack of workflow guidance, too many clicks to confirm order state.

3. **The Detail-Oriented Manager**
   - Goal: Check every order for accuracy before submission.
   - Pain Points: Missing confirmation that edits saved, no cancel option during edit, unclear if order type can change.

4. **The Late-Night Customer**
   - Goal: Provide quick takeaway orders without need for a full POS walkthrough.
   - Pain Points: Too much interface text, uncertain whether the to-go selection is locked, unclear submission flow.

5. **The Owner/Quality Auditor**
   - Goal: Ensure the system is robust and easy to maintain.
   - Pain Points: Deployment path issues, reliance on local files, inconsistent order numbering after reload.

## Testing Results

### Friction Points Discovered

- **Unclear order creation workflow**: Users were not sure what happened after clicking `Add New Order`.
- **Save vs Submit confusion**: It was difficult to distinguish between saving edits and submitting the final order.
- **Editing order type risk**: The dine-in/to-go selection could be changed mid-edit in a way that broke order intent.
- **No cancel action**: During editing, users could not cancel without losing track of the order.
- **Poor session feedback**: There was no summary of how many orders were active in the current session.
- **Deployment file path failure**: Using local Mac filesystem paths caused `FileNotFoundError` on remote hosted environments.

## Transformation

### What Changed

- Added a clear top-level explanation in the `Manage Orders` view to describe the workflow: `Add New Order`, `Edit`, `Save Changes`, and `Submit`.
- Added a caption showing the number of current session orders.
- Added a success message when a new order is created, making the workflow feel responsive.
- Added a `Cancel` button on the edit screen so users can back out of changes safely.
- Disabled the dine-in/to-go radio once an order is saved, preventing accidental order-type changes.
- Switched the menu source to the GitHub raw URL for `menu.txt`, so the app reads the shared project data rather than a local machine path.
- Switched order log and receipt file paths to app-relative storage so the app works correctly in deployment.

### Before and After Screenshots

- **Before**: `before_manage_orders.png`
- **After**: `after_manage_orders.png`

> Note: Replace the screenshot placeholders above with actual UI screenshots captured from the Streamlit app.
