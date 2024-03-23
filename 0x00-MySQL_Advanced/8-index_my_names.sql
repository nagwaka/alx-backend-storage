--- create an index idx_name_first on the table names and the first letter of name.

CREATE INDEX IF NOT EXISTS idx_name_first ON names (LEFT(name, 1));
