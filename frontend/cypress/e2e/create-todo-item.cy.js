describe('Logging into the system & Creating task', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let title // Title of the task
  let uTubeURL // URL of an optional u tube video when creating a task.
  let taskId // Task Id
  let todoItemName // Todo item name

  beforeEach(() => {
    // Create user first
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((resUser) => {
        uid = resUser.body._id.$oid;
        name = user.firstName + ' ' + user.lastName;
        email = user.email;
        cy.log('Created user ID: ' + uid);

        // Log in
        cy.visit('http://localhost:3000');
        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email);
        cy.get('form').submit();

        // Load task fixture data
        cy.fixture('task.json').then((task) => {
          task.userid = uid;
          title = task.title;
          uTubeURL = task.url;

          // Intercept the request before submitting the form in order to get the taskId after the task creation.
          cy.intercept('POST', '**/tasks/create').as('createTask');

          cy.contains('div', 'Title').find('input[type=text]').type(title);
          cy.contains('div', 'YouTube URL').find('input[type=text]').type(uTubeURL);
          cy.get('form').submit();

          // Waiting for the network call to complete
          cy.wait('@createTask').then((interception) => {
            const responseBody = interception.response.body;

            // Storing the taskId
            taskId = responseBody?._id?.$oid || responseBody[0]?._id?.$oid;
            cy.log('Task Created: ' + taskId);
          });
        });
      });
    });
  });

  it('Creating a task', () => {
    cy.contains('div', 'Title')
      .find('input[type=text]')
      .type(title);

    cy.contains('div', 'YouTube URL')
      .find('input[type=text]')
      .type(uTubeURL);

    cy.get('form').submit();

    // Asserting that task is shown on the UI (Optional).
    cy.contains(title).should('exist');

    // Now click on the task created in order to display the Todo items.
    cy.get('div.title-overlay')
      .contains(title)
      .click();

    cy.fixture("todo.json").then((todoItem) => {
      todoItemName = todoItem.itemName;
      cy.get("div.popup")
        .find("input[type=text]")
        .type(todoItemName)

      cy.get("form.inline-form")
        .find("input[type=submit]")
        .click();

      // Mking sure that the todo item has been created & its name is todoItemName.
      cy.get("li.todo-item").should('contain', todoItemName);

      // Toggle the todo item from Unchecked to checked.
      cy.get("li.todo-item").contains(todoItemName)
        .parents("li.todo-item")
        .find('span.checker.unchecked').click();

      cy.get('li.todo-item').contains(todoItemName)
        .parents("li.todo-item")
        .find("span.checker")
        .should('have.class', 'checker checked');

        //Alternative senario toggle it from ckecked to unchecked.
        cy.get('li.todo-item').contains(todoItemName)
        .parents("li.todo-item")
        .find("span.checker.checked").click();

        cy.get('li.todo-item').contains(todoItemName)
        .parents("li.todo-item")
        .find("span.checker")
        .should('have.class', 'checker unchecked');

        //Remove todo item by clicking on the X that has class remover.
        cy.get('li.todo-item').contains(todoItemName)
          .parents("li.todo-item")
          .find("span.remover").click();

        // Assert the item no longer exists
        cy.get('li.todo-item').contains(todoItemName).should('not.exist');
    })
  });

  it("Alternative senario", () => {
    // Alternative senario: If the description is empty, then the “Add” button should remain disabled.

    // Click on the task created in order to display the Todo items.
    cy.get('div.title-overlay')
      .contains(title)
      .click();

    cy.get("div.popup")
    .find("input[type=text]").should('have.value', '');

    cy.get("form.inline-form")
      .find("input[type=submit]").should('be.disabled');
  });

  afterEach(() => {
    // Only attempt to delete if we have valid IDs

    if (taskId) {
      cy.log('Attempting to delete task with ID: ' + taskId);
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/tasks/byid/${taskId}`,
        failOnStatusCode: false // Continue even if this request fails
      }).then((response) => {
        cy.log(`Task deletion response status: ${response.status}`);
      });
    } else {
      cy.log('No task ID available to delete');
    }

    if (uid) {
      cy.log('Attempting to delete user with ID: ' + uid);
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`,
        failOnStatusCode: false // Continue even if this request fails
      }).then((response) => {
        cy.log(`User deletion response status: ${response.status}`);
      });
    } else {
      cy.log('No user ID available to delete');
    }
  });
});