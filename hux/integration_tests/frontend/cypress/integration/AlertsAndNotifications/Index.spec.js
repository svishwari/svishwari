import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Notifications", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to view a list of notifications", () => {
    cy.location("pathname").should("eq", route.home)

    //notification bell icon should be visible
    cy.get(selector.notification.notificationicon).should("be.visible")
    //click on the bell button
    cy.get(selector.notification.notificationicon).click()
    // open open notification drop down and check the length of the data
    cy.get(selector.notification.notificationlistmenu).should(($menulist) => {
      expect($menulist).to.have.length(5)
    })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    // view all link should be visible
    cy.get(selector.notification.viewAllNotifications).should("be.visible")
    // click on the view all link
    cy.get(selector.notification.viewAllNotifications).click()
    // route in notification screen
    cy.location("pathname").should("eq", route.notifications)
    // scroll down for lazy loading
    cy.scrollTo("bottom", { duration: 1000 })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    // scroll up to click the return button
    cy.scrollTo("top", { duration: 1000 })
    // click on the return to previous page button
    cy.get(selector.notification.notificationReturnButton).click()
  })
})