Feature: Handling Images in the Catalog
  @dont_clear
  Scenario: Uploading Images
    Given the user has a folder of images for labeling
    And the user selected a bunch of images in the folder
    When selected the upload option
    Then return the information to the user
    And the api should upload each image to the filesystem
    And save the upload information to the cache

  Scenario: Downloading Images
    Given the user has an uploaded image
    When the user calls the system to download the given image
    Then the api downloaded the image from the filesystem