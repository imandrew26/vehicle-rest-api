-- Database schema
CREATE TABLE Vehicles (
    VIN VARCHAR(17) PRIMARY KEY,
    ManufacturerName VARCHAR(100),
    Description TEXT,
    HorsePower INT,
    ModelName VARCHAR(100),
    ModelYear INT,
    PurchasePrice DECIMAL(10, 2),
    FuelType VARCHAR(50)
);

-- Case-insensitivity for VIN
CREATE UNIQUE INDEX UQ_Vehicles_VIN ON Vehicles (LOWER(VIN));