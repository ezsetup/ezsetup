create type DEPLOY_STATUS as enum ('inactive', 'deploying', 'deployfailed', 'active', 'destroying', 'destroyfailed');
create type REQUEST_STATUS as enum ('pending', 'accepted');
create type REQUEST_TYPE as enum ('join', 'leave');
create type CLOUD_PROVIDER as enum ('Openstack', 'AWS', 'GCloud', 'Azure');

-- app-independent users table
create table users (id SERIAL PRIMARY KEY,
                    email TEXT unique,
                    fullname TEXT,
                    hash TEXT,
                    is_root BOOLEAN DEFAULT FALSE);


-- app-specific user info
create table userinfos(id SERIAL PRIMARY KEY,
                       user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                       UNIQUE (user_id),
                       permission_groups TEXT[]
                      );

create table scenarios (id SERIAL PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        topo JSONB,
                        is_public BOOLEAN,
                        owner_id INTEGER REFERENCES users (id) ON DELETE CASCADE,
                        UNIQUE (name, owner_id));

create table labs (id SERIAL PRIMARY KEY,
                  name TEXT,
                  description TEXT,
                  status DEPLOY_STATUS,
                  owner_id INTEGER REFERENCES users (id) ON DELETE CASCADE,
                  scenario_id INTEGER REFERENCES scenarios (id) ON DELETE SET NULL);

create table cloudconfigs (id SERIAL PRIMARY KEY,
                     detail JSONB,
                     provider CLOUD_PROVIDER,
                     lab_id INTEGER REFERENCES labs(id) ON DELETE CASCADE,
                     UNIQUE (lab_id));


create table slices (id SERIAL PRIMARY KEY,
                    lab_id INTEGER REFERENCES labs (id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    name TEXT,
                    cloud_attrs JSONB,
                    status DEPLOY_STATUS);

create table labrequests(id SERIAL PRIMARY KEY,
                        lab_id INTEGER REFERENCES labs(id) ON DELETE CASCADE,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        request_type REQUEST_TYPE,
                        status REQUEST_STATUS,
                        UNIQUE (user_id, lab_id));


create table networks (id SERIAL PRIMARY KEY,
                          name TEXT,
                          cidr TEXT,
                          status DEPLOY_STATUS,
                          x INTEGER,
                          y INTEGER,
                          cloud_attrs JSONB,
                          gid TEXT,
                          slice_id INTEGER REFERENCES slices(id) ON DELETE CASCADE);


create table instances (id SERIAL PRIMARY KEY,
                          name TEXT,
                          public_ip TEXT,
                          status DEPLOY_STATUS,
                          password TEXT,
                          x INTEGER,
                          y INTEGER,
                          gid TEXT,
                          cloud_attrs JSONB,
                          links JSONB[], -- [{network_id, ip}]
                          image TEXT,
                          configurations JSONB[], -- list of software configurations
                          flavor JSONB, -- flavor (name, ram) information
                          slice_id INTEGER REFERENCES slices(id) ON DELETE CASCADE);

create table routers (id SERIAL PRIMARY KEY,
                          name TEXT,
                          public_ip TEXT,
                          status DEPLOY_STATUS,
                          password TEXT,
                          x INTEGER,
                          y INTEGER,
                          gid TEXT,
                          cloud_attrs JSONB,
			  links JSONB[], -- [{network_id, ip}]
                          image TEXT,
                          configurations JSONB[], -- list of software configurations
                          flavor JSONB, -- flavor (name, ram) information
                          slice_id INTEGER REFERENCES slices(id) ON DELETE CASCADE);
