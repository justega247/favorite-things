#### How long did you spend on the coding test below?
100 hours

#### What would you add to your solution if you had more time?
I would add Image upload capabilities for the categories
I would authenticate the API and restrict users to only be able to view/edit category and favorite things they created.

#### What was the most useful feature that was added to the latest version of your chosen language?
The feature I found the most useful while working on this project is the built-in breakpoint introduced in python 3.7. It makes using the python debugger more flexible and intuitive

##### Code Snippet
```
        for i in range(0, len(all_history) - 1):
            new_history, old_history = all_history[i], all_history[i + 1]
            delta = new_history.diff_against(old_history)
            changes = changes + delta.changes
        breakpoint()
        for change in changes:
            response.append(f'{change.field.capitalize()} changed from {change.old} to {change.new}')
        return Response({
            "audit": response
        })
```

#### How would you track down a performance issue in production? 
 The steps I would take in tracking down performance issues are

- Investigate the issue before making any hypothesis about it
- Try to reproduce the issue locally or in a test environment using the information gathered from my investigation
- Find out at what point the issue was introduced on production

#### Have you ever had to do this?
Yes