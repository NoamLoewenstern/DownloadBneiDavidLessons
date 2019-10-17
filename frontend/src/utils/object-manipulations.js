export const jsonify = string => {
	try {
		return JSON.parse(string);
	} catch (e) {
		return null;
	}
};
