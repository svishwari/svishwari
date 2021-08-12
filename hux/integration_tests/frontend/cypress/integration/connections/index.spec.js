import route from "../../support/routes.js";

const selector = {
  home: {
    // TODO: add a better selector for this button in the UI
    signin: "button",
  },
  login: {
    email: "input[id=okta-signin-username]",
    password: "input[id=okta-signin-password]",
    submit: "input[id=okta-signin-submit]",
  },
  _datasources_: "div[data-e2e='e2edataSourcesList']",
  _destinations_: "div[data-e2e='e2edestinationsList']",
  _dataSourcesAdd_: {
    firstcondition:"div[tabindex='0']",
    secondcondition:"div[data-e2e='e2edataSourcesAddList']"
  },
  connections: "a[href='/connections']",
  addDataSource: "a[href='/datasources/add?select=true']",
}

describe("Tests data souces and destinations in connections", () => {
  before(() => {
    // opens the app
    cy.visit(route.home);

    // clicks the signin button
    cy.get(selector.home.signin).click();

    // we should now be on the login page
    cy.location("pathname").should("eq", route.login);

    // fill in the form
    cy.get(selector.login.email)
      .type(Cypress.env("USER_EMAIL"), { log: false });

    cy.get(selector.login.password)
      .type(Cypress.env("USER_PASSWORD"), { log: false });

    // submit the form
    cy.get(selector.login.submit).click();

    // TODO: add MFA related authentication if needed

    // we should no longer be on the login page
    cy.location("pathname", { timeout: 10000 })
      .should("not.eq", route.login)
      .then(() => {
        // okta does its authentication... 
        // once its done, we should be redirected back to the app
        cy.location("pathname")
          .should("eq", route.oktaSignInRedirectURI);
      })
  });

  it("testing data management > connections > data sources", () => {
    cy.location("pathname").should("eq", route.overview);

    //click on connections on side nav bar
    cy.get(selector.connections).click();
    cy.location("pathname").should("eq", route.connections);

    //validate data sources exist by getting total no. of them
    cy.get(selector._datasources_).its("length").as("dataSourcesCount");
    
    //add a data source
    cy.get(selector.addDataSource).click();
    cy.location("pathname").should("eq", route.addDataSource);
    cy.get(selector._dataSourcesAdd_.firstcondition + selector._dataSourcesAdd_.secondcondition).eq(0).click()
    cy.get("button").contains("Add 1 data source").click();
    cy.location("pathname").should("eq", route.connections);
    
    //wait for 1 sec for change to happen
    cy.wait(1000)

    //make sure that number of data sources have increased by 1
    cy.get("@dataSourcesCount").then(dataSourcesCount => {
      cy.get(selector._datasources_).its("length").should('eq',dataSourcesCount+1);

      //validate correct status on all added data sources
      cy.get(selector._datasources_).as("dataSourcesList");
      for(let index=0;index<dataSourcesCount;index++){
        cy.get("@dataSourcesList").eq(index).contains("Active");
      }
      cy.get("@dataSourcesList").eq(dataSourcesCount).contains("Pending");
    });
  });

  it("testing data management > connections > destinations", () => {
    cy.location("pathname").should("eq", route.connections);
    cy.get(selector._destinations_).its("length").should('be.gt',0);
  });

});
