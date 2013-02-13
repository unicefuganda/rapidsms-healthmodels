Feature: Updating facility

 Scenario: Changes to HealthFacility should be logged
   Given I am logged in as admin
   And I have an existing facility with UID
   When I edit a HealthFacility
   And I attempt to save
   Then I should see my facility changes are made
   And I should see my changes are logged

 Scenario: Unsuccessful Changes to HealthFacility should create failure
   Given I am logged in as admin
   And I dont have an existing facility with UID
   When I edit a HealthFacility
   And I attempt to save
   Then I should see an error
   And I should have a failure object created to report it
