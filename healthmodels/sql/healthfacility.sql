CREATE OR REPLACE FUNCTION create_supplypoint() RETURNS TRIGGER AS $create_supplypoint$
    DECLARE
    x INTEGER;
    y INTEGER;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            SELECT INTO x id FROM logistics_supplypoint WHERE code = NEW.code;
            SELECT INTO y id FROM healthmodels_healthfacilitybase WHERE  code = NEW.code;
            UPDATE healthmodels_healthfacility SET supply_point_id = x WHERE  healthfacilitybase_ptr_id = y;
            RETURN NEW;
        END IF;
    END;
$create_supplypoint$ LANGUAGE plpgsql;

CREATE TRIGGER create_supplypoint AFTER INSERT ON logistics_supplypoint
    FOR EACH ROW EXECUTE PROCEDURE create_supplypoint();
